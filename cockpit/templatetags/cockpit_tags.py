from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.templatetags.admin_list import ResultList, results, lookup_field, result_headers, result_hidden_fields
from django.utils.html import remove_tags


register = template.Library()


def find_roots(nodes, searchOnlyParentless=True):
    roots = []
    for qry in nodes:
        if qry.parent_id is None:
            roots.append(qry)
        elif searchOnlyParentless is not True:
            hasParent = False
            for qryin in nodes:
                if qryin.id == qry.parent_id:
                    hasParent = True
                    break
            if not hasParent:
                roots.append(qry)
    return roots


def find_children(node, nodes):
    children = []
    for qry in nodes:
        if qry.parent_id == node.id:
            children.append(qry)
    return children


class CockpitPageTreeNode(template.Node):
    def __init__(self, template_nodes, queryset_var):
        self.template_nodes = template_nodes
        self.queryset_var = queryset_var

    def _render_node(self, context, node, nodes):
        bits = []
        context.push()
        for child in find_children(node, nodes):
            context['node'] = child
            bits.append(self._render_node(context, child, nodes))
        context['node'] = node
        context['children'] = mark_safe(u''.join(bits))
        rendered = self.template_nodes.render(context)
        context.pop()
        return rendered

    def render(self, context):
        queryset = self.queryset_var.resolve(context)
        roots = find_roots(queryset)
        bits = [self._render_node(context, node, queryset) for node in roots]

        return ''.join(bits)

@register.tag
def cockpit_page_tree(parser, token):
    """
    Iterates over the nodes in the tree, and renders the contained block for each node.
    This tag will recursively render children into the template variable {{ children }}.

    Example Usage:
            <ul>
            {% cockpit_page_tree pages %}
                <li><a href="{% url 'cockpit:detail' slug=node.slug %}">{{ node.heading }}</a>
                    <ul class="children">
                        {{ children }}
                    </ul>
                </li>
            {% end_cockpit_page_tree %}
            </ul>
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a queryset') % bits[0])

    queryset_var = template.Variable(bits[1])

    template_nodes = parser.parse(('end_cockpit_page_tree',))
    parser.delete_first_token()

    return CockpitPageTreeNode(template_nodes, queryset_var)


class CockpitPageResultList(ResultList):
    def __init__(self, form, *items):
        self.form = form
        super(ResultList, self).__init__(*items)


def append_children_page_list(unordered_list, ordered_list, item, hierarchy_levels, order):
    ordered_list.append(item)
    hierarchy_levels.append(order)
    #unordered_list.remove(item)

    for child in find_children(item, unordered_list):
        order_in_child = order + 1
        append_children_page_list(unordered_list, ordered_list, child, hierarchy_levels, order_in_child)


def create_ordered_page_list(unordered_list):
    roots = find_roots(unordered_list, searchOnlyParentless=False)
    ordered_list = []
    hierarchy_levels = []
    for root in roots:
        append_children_page_list(unordered_list, ordered_list, root, hierarchy_levels, 0)
    return {'ordered_list': ordered_list,
            'hierarchy_levels': hierarchy_levels}

@register.inclusion_tag("admin/change_list_results.html")
def cockpit_page_result_list(cl):
    """
    Displays the headers and data list together
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1

    page_results = cl.result_list
    ordered_results = create_ordered_page_list(page_results)
    cl.result_list = ordered_results['ordered_list']
    hierarchy_levels = ordered_results['hierarchy_levels']
    list_results = list(results(cl))
    i = 0
    for result in list_results:
        result[1] = remove_tags(result[1], "th")
        result[1] = mark_safe(u"<th style='padding-left: %dpx;'>%s</th>" % (5 + hierarchy_levels[i] * 20, result[1]))
        i += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list_results}