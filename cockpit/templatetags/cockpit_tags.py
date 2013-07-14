from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = template.Library()


def find_roots(nodes):
    roots = []
    for qry in nodes:
        if qry.parent_id is None:
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
