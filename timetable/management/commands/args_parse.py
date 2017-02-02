import os, argparse

def parser_argparser(parser, subparser_class=None):
	parser.add_argument('--term-and-year', nargs=2, type=str,
		help='parse for term and year - two args') 
	parser.add_argument('--department', default='all',
		help='parse specific department by code')
	parser.add_argument('-o', '--output', action=writable_file_action,
		help='(default:  scripts/[school]/data/courses.json)')
	parser.add_argument('--hide-progress-bar', dest='hide_progress_bar', action='store_true', default=False,
		help='flag to hide progress bar (default is visible)')

	textbooks = parser.add_mutually_exclusive_group()
	textbooks.add_argument('--textbooks', dest='textbooks', action='store_true',
		help='parse textbooks')
	textbooks.add_argument('--no-textbooks', dest='textbooks', action='store_false',
		help='don\'t parse textbooks')
	textbooks.set_defaults(textbooks=False)

	validation = parser.add_mutually_exclusive_group()
	validation.add_argument('--validate', dest='validate', action='store_true',
		help='validate parser output (default)')
	validation.add_argument('--no-validate', dest='validate', action='store_false',
		help='do not validate parser output')
	validation.set_defaults(validate=True)

def validator_argparser(parser):
	parser.add_argument('--output-error', help='(default:  %(default)s)', action=writable_file_action)
	parser.add_argument('--config-file', dest='config_file', metavar='', action=None,
		help='pull config file from this path')
	break_error = parser.add_mutually_exclusive_group()
	break_error.add_argument('--break-on-error', dest='break_on_error', action='store_true', help='(default)')
	break_error.add_argument('--no-break-on-error', dest='break_on_error', action='store_false')
	break_error.set_defaults(break_on_error=True)
	break_warning = parser.add_mutually_exclusive_group()
	break_warning.add_argument('--break-on-warning', dest='break_on_warning', action='store_true')
	break_warning.add_argument('--no-break-on-warning', dest='break_on_warning', action='store_false', help='(default)')
	break_warning.set_defaults(break_on_warnings=False)

def digestor_argparser(parser, writable_file_action=None):
	parser.add_argument('--strategy', default='burp', choices=['vommit', 'absorb', 'burp', 'dbdiff', 'dbload', 'dbdiff_and_dbload'])

# Argparse hook to check for writable file within directory
class writable_file_action(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		prospective_file = values
		prospective_dir = os.path.dirname(os.path.abspath(prospective_file))
		if not os.path.isdir(prospective_dir):
			raise parser.error('writable_file: `%s` is not a valid file path' % (prospective_file) )
		if os.access(prospective_dir, os.W_OK):
			setattr(namespace, self.dest, prospective_file)
		else:
			raise parser.error('writable_file: `%s` is not a writable file' % (prospective_file) )

# Setup Object for creating valid Django subparsers
# REF: http://stackoverflow.com/questions/36706220/is-it-possible-to-create-subparsers-in-a-django-management-command
# class SubParser(CommandParser):
# 	def __init__(self, **kwargs):
# 		super(SubParser, self).__init__(cmd, **kwargs)

# FIXME --no-validate and validator conflict without resolutoin
# validator_sub_parser = parser.add_subparsers(title="validator", parser_class=SubParser, help='options when validating parser output')
# validator = validator_sub_parser.add_parser('validator', help='run python manage.py parse [school] validator --help for more')
# validator_argparser(validator)
