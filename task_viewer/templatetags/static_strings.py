from django import template

register = template.Library()

def project_name():
	project_name = 'kulTasker'
	return project_name

register.simple_tag(project_name)