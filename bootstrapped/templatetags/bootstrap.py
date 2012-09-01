from django import template
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

register = template.Library()

SCRIPT_TAG = '<script src="%sjs/bootstrap-%s.js" type="text/javascript"></script>'

class BootstrapJSNode(template.Node):

    def __init__(self, args):
        self.args = set(args)

    def render_all_scripts(self):
        results = [
#            SCRIPT_TAG % (settings.STATIC_URL, 'jquery'),
            '<script src="%sjs/bootstrap.min.js" type="text/javascript"></script>' % settings.STATIC_URL,
            SCRIPT_TAG % (settings.STATIC_URL, 'affix'),
            SCRIPT_TAG % (settings.STATIC_URL, 'alert'),
            SCRIPT_TAG % (settings.STATIC_URL, 'button'),
            SCRIPT_TAG % (settings.STATIC_URL, 'carousel'),
            SCRIPT_TAG % (settings.STATIC_URL, 'collapse'),
            SCRIPT_TAG % (settings.STATIC_URL, 'dropdown'),
            SCRIPT_TAG % (settings.STATIC_URL, 'modal'),
            SCRIPT_TAG % (settings.STATIC_URL, 'popover'),
            SCRIPT_TAG % (settings.STATIC_URL, 'scrollspy'),
            SCRIPT_TAG % (settings.STATIC_URL, 'tab'),
            SCRIPT_TAG % (settings.STATIC_URL, 'tooltip'),
            SCRIPT_TAG % (settings.STATIC_URL, 'transition'),
            SCRIPT_TAG % (settings.STATIC_URL, 'typeahead'),
        ]
        return '\n'.join(results)

    def render(self, context):
        if 'all' in self.args:
            return self.render_all_scripts()
        else:
            tags = [SCRIPT_TAG % (settings.STATIC_URL,tag) for tag in self.args]
            return '\n'.join(tags)

@register.simple_tag
def bootstrap_custom_less(less):
    output=[
            '<link rel="stylesheet/less" type="text/css" href="%s%s" media="all">' % (settings.STATIC_URL, less),
            '<script src="%sjs/less-1.3.0.min.js" type="text/javascript"></script>' % settings.STATIC_URL,
        ]
    return '\n'.join(output)

@register.simple_tag
def bootstrap_css(responsive=False):
    min = ''
    if not settings.TEMPLATE_DEBUG:
        min = '.min'
    output = ['<link rel="stylesheet" type="text/css" href="%sbootstrap%s.css">' % (settings.STATIC_URL, min)]
    if responsive == 'responsive':
        output.append('<link rel="stylesheet" type="text/css" href="%sbootstrap-responsive%s.css">' % (settings.STATIC_URL, min))
    return '\n'.join(output)

@register.simple_tag
def bootstrap_less(responsive=False):
    output=['<link rel="stylesheet/less" type="text/css" href="%sless/bootstrap.less">' % settings.STATIC_URL,]
    if responsive == 'responsive':
        output.append('<link rel="stylesheet/less" type="text/css" href="%sless/responsive.less">' % settings.STATIC_URL)
    output.append('<script src="%sjs/less-1.3.0.min.js" type="text/javascript"></script>' % settings.STATIC_URL)
    return '\n'.join(output)

@register.tag(name='bootstrap_js')
def do_bootstrap_js(parser, token):
    #print '\n'.join(token.split_contents())
    return BootstrapJSNode(token.split_contents()[1:])
    
    
    
#this has been merged from django-bootstrap-form
@register.filter
def bootstrapform(element):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        template = get_template("bootstrapform/field.html")
        context = Context({'field': element})
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            template = get_template("bootstrapform/formset.html")
            context = Context({'formset': element})
        else:
            template = get_template("bootstrapform/form.html")
            context = Context({'form': element})
        
    return template.render(context)

@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"


@register.filter
def is_radio(field):
    return field.field.widget.__class__.__name__.lower() == "radioselect"
