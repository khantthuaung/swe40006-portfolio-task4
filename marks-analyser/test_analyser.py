import tempfile
from pathlib import Path
import unittest
from analyser import grade_for, make_report, read_students


class AnalyserTests(unittest.TestCase):
    def test_boundaries(self):
        for mark, grade in [(0, 'F'), (49.99, 'F'), (50, 'P'), (60, 'C'),
                            (70, 'D'), (80, 'HD'), (100, 'HD')]:
            self.assertEqual(grade_for(mark), grade)

    def test_invalid_rows(self):
        students, errors = read_students('data/invalid-students.csv')
        self.assertEqual(len(students), 1)
        self.assertEqual(len(errors), 7)

    def test_report(self):
        students, errors = read_students('data/students.csv')
        report = make_report(students, errors)
        self.assertIn('Average mark: 63.80', report)
        self.assertIn('Pass rate: 80.00%', report)
        self.assertEqual(errors, [])

    def test_missing_headers(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'bad.csv'
            path.write_text('name,score\nAlex,85\n')
            with self.assertRaises(ValueError):
                read_students(path)

    def test_empty_report(self):
        self.assertIn('No valid marks to analyse.', make_report([], []))


if __name__ == '__main__':
    unittest.main()
