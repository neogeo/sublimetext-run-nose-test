import sublime
import sublime_plugin


# Author: Andrew Ozor
# Description: Copies the nosetest command, to run a given test, into the clipboard
class RunNoseTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_syntax_file('Packages/Python/Python.tmLanguage')

        if len(self.view.file_name()) > 0:
            file_name = self.view.file_name()
            if file_name.find('tests'):
                test_class = file_name.split('/')[-1][0:-3]
                test_class = test_class.title().replace('_', '')

                test_path = file_name[file_name.find('tests'):-3].replace('/', '.')

                # FIXME: Get the class name better. for each line, go up until you find 'class'
                # regs = self.view.find_all('class')
                # print(regs)

                # copy line
                for region in self.view.sel():
                    line = self.view.line(region)
                    line_contents = self.view.substr(line)

                    def_index = line_contents.find('def')
                    paren_index = line_contents.find('(')
                    if def_index != -1 and paren_index != -1:
                        test_method_name = line_contents[def_index + 4:paren_index]

                        command = 'nosetests -s -v {}:{}.{}'.format(test_path, test_class, test_method_name)
                        sublime.set_clipboard(command)
                    else:
                        sublime.status_message('Not a python test method')
                        return

                # self.view.insert(edit, line.begin(), line_contents)
                sublime.status_message('Copied file path {}'.format(test_path))
            else:
                sublime.status_message('Not a python test file')

    def is_enabled(self):
        return self.view.file_name() is not None and len(self.view.file_name()) > 0 and '.py' in self.view.file_name() and 'test' in self.view.file_name()
