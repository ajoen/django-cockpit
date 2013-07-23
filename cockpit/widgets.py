from itertools import chain
from django.db.models.query import QuerySet
from django.forms import widgets
from django.utils.html import format_html, mark_safe
from django.utils.encoding import force_text
from cockpit.templatetags.cockpit_tags import create_ordered_page_list


class CockpitPageSelectWidget(widgets.Select):
    def render_option_page(self, selected_choices, option, hierarchical_order):
        """
        Renders the page by putting '-' according to the hierarchical order of the page.
        :param selected_choices: Selected choices
        :param option: Page choice to render
        :param hierarchical_order: Hierarchical order (depth) of the Page choice
        :return:
        """
        option_value = force_text(option.id)
        option_label = force_text(option)
        for i in range(0, hierarchical_order):
            option_label = "-" + option_label
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}>{2}</option>',
                           option_value,
                           selected_html,
                           option_label)

    def render_options(self, choices, selected_choices):
        """
        Overrides 'widgets.Select.render_options' to render hierarchical order in the select box.
        """
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []

        # Order pages hierarchically
        ordered_choices = create_ordered_page_list(self.choices.queryset, searchOnlyParentless=True)

        # Append the 'None' choice
        output.append(self.render_option(selected_choices, "", "-----------"))

        # Append other pages
        i = 0
        for choice in ordered_choices['ordered_list']:
            output.append(self.render_option_page(selected_choices,
                                                  choice,
                                                  ordered_choices['hierarchy_levels'][i]))
            i += 1
        return '\n'.join(output)