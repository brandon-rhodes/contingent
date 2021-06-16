from contingent.projectlib import Project, Task
#from textwrap import dedent
from unittest import TestCase

class Tests(TestCase):
    def test_whether_dangling_targets_are_cleaned_up(self):
        project = Project()
        task = project.task

        @task
        def read(filename):
            return content

        @task
        def hash_of(filename):
            return sum(ord(c) for c in read(filename)) % 256

        @task
        def render(filename):
            content = read(filename)
            if '$HASH' in content:
                content = content.replace('$HASH', str(hash_of(filename)))
            return content

        # First check: with simple content, render() should depend only
        # on the output of read().

        content = 'A file.'

        project.start_tracing()
        self.assertEqual(render('text.txt'), 'A file.')
        trace = project.stop_tracing()

        self.assertEqual(trace.splitlines(), [
            "calling render('text.txt')",
            ". calling read('text.txt')",
        ])

        # Second check: with more interesting content, render() will
        # also call hash().

        content = 'My hash is $HASH.'
        print(project._cache)

        t = Task(read, ('text.txt',))
        print(t)
        print(t in project._cache)

        project.invalidate(t)

        project.start_tracing()
        project.rebuild()
        trace = project.stop_tracing()

        self.assertEqual(render('text.txt'), 'My hash is 28.')

        self.assertEqual(trace.splitlines(), [
            "calling read('text.txt')",
            "calling render('text.txt')",
            ". calling hash_of('text.txt')",
        ])

        # Final check: if we then remove the interesting content, does
        # Contingent recognize the hash no longer needs to be computed?

        content = 'Simple file again.'
        print(project._cache)

        t = Task(read, ('text.txt',))
        print(t)
        print(t in project._cache)

        project.invalidate(t)

        project.start_tracing()
        project.rebuild()
        trace = project.stop_tracing()

        self.assertEqual(render('text.txt'), 'Simple file again.')

        self.assertEqual(trace.splitlines(), [
            "calling read('text.txt')",
            "calling render('text.txt')",
        ])
