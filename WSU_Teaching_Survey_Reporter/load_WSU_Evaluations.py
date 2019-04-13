import pandas as pd
import numpy as np
import os as os
import PyQt5.QtWidgets as QtWidgets
import re


def append(*args):
    for i, name in enumerate(args):
        if i is 0:
            combined = args[i]
        else:
            combined = combined.append(args[i], ignore_index=True)
    return combined


def load_evals(filename):
    df = pd.read_excel(filename, sheet_name='RawData')
    term = (filename[filename.find('201'):filename.find('courses')][0:4] +
            " " +
            filename[filename.find('201'):filename.find('courses')][6:])

    # List of unique faculty
    facultynames = df["InstructorName"].unique()

    # List of question headers
    list_of_headers = list(df)
    for i, header in enumerate(list(df)):
        if "Question" not in header:
            list_of_headers.remove(header)
    # print(list_of_headers)

    for name in facultynames:
        facultysevals = df.loc[df['InstructorName'] == name]
        facultycourses = sorted(facultysevals["CourseTitle"].unique())
        # print(name, '\n'.join(facultycourses))

    pre_headers = ["Instructor", "Term", "Class", "Question", "Responses"]
    # pre_headers

    for i, name in enumerate(facultynames):
        facultysevals = df.loc[df['InstructorName'] == name]
        facultycourses = sorted(facultysevals["CourseTitle"].unique())
        for j, coursename in enumerate(facultycourses):
            coursename_short = coursename[:coursename.find(
                '-', 4)].replace('-', ' ')
            coursename_short = coursename_short.replace('  ', ' ').rstrip()
            # print(coursename_short)
            for k, question in enumerate(list_of_headers):
                # print(i,j,k)
                question_list_non_scantron = [
                    """Describe the overall effectiveness of this
                       instructor.""",
                    """Did the instructor evaluate your work based on the
                       expectations described in the course syllabus?""",
                    """Did the instructor routinely start class on time and use
                       the full class period?""",
                    """How did the instructor demonstrate interest in your
                       learning?""",
                    """How effectively did the instructor communicate both in
                       and out of the classroom?""",
                    """Were the course content and lectures well organized?""",
                    """Was the instructor reasonably available and responsive
                       to your needs during office hours and appointments, or
                       on line?""",
                    """Do you have any additional, relevant comments?."""]

                question_list_scantron = [
                    """Your registration is:""",
                    """Your college/school is:""",
                    """You are taking this course as a(n)""",
                    """The instructor was available for consultation.""",
                    """Student responsibilities for this course were well
                       defined.""",
                    """Class time was well spent.""",
                    """I learned a lot from the instructor in this course.""",
                    """Course materials contributed to my learning.""",
                    """I was challenged in this course.""",
                    """Coming into this course I was motivated to learn this
                       subject.""",
                    """Please comment on aspects of the instructor's teaching,
                       such as clarity of explanations and examples, handling
                       of questions, stimulation of thinking, and respect for
                       individuals and their differences.""",
                    """Did the instructor aid in your understanding of this
                       subject?  Please give specific examples consistent with
                       your response.""",
                    """Please comment further on any of the items which you
                       were asked about in this evaluation.""",
                    """Additional comments"""
                    ]

                if 'cantron' in filename:
                    survey_question = question_list_scantron[k]
                else:
                    survey_question = question_list_non_scantron[k]
                survey_question = re.sub('\n ', ' ', survey_question)
                survey_question = re.sub(' +', ' ', survey_question)

                # print(name)
                # print(coursename)
                instructor_data = df.loc[df['InstructorName'] == name]
                # print(instructor_data)
                instructors_course_data = instructor_data.loc[instructor_data['CourseTitle'] == coursename]
                # print(instructors_course_data)

                answers = instructors_course_data[question]
                # print(answers)
                answers = answers.dropna()
                if len(answers) > 0 and isinstance(answers.iloc[0], str):
                    # print(answers.dropna())
                    cell_value = '. :: '.join(answers)
                    cell_value = cell_value.replace('..', '.')
                    cell_value = cell_value.replace('. .', '.')
                    cell_value = '[' + survey_question + ']  ' + cell_value
                    cell_value = cell_value.replace('..', '.')
                else:
                    if len(answers) > 0:
                        cell_value = np.mean(np.array(answers).T)
                        # print(answers)
                        # print('average', cell_value)
                    else:
                        cell_value = 0

                rowdata = [name, term, coursename_short, question, cell_value]
                new_df = dict(zip(pre_headers, rowdata))
                new_sheet_part = pd.DataFrame(new_df, index=[0])
                if i + j + k is 0:
                    new_sheet = new_sheet_part
                    # print(new_sheet)
                    # print('start now!')
                else:
                    # print(new_sheet_part)
                    new_sheet = new_sheet.append(
                        new_sheet_part, ignore_index=True)
    return new_sheet


'''def gui_fname(dir=None):
    """Select a file via a dialog and return the file name."""
    if dir is None:
        dir = './'
    fname = QFileDialog.getOpenFileName(
        None,
        "Select data file...",
        dir,
        filter="All files (*);; Some Files (*201*.xlsx)")
    return fname[0]'''


def openfile_dialog():
    # from PyQt5 import QtGui, QtWidgets
    dir = './'
    app = QtWidgets.QApplication([dir])
    fname = QtWidgets.QFileDialog.getOpenFileName(
        None, "Select a file...", '.', filter="All files (*)")
    return str(fname)


def load_all_evals(path='/Users/jslater/Documents/Admin/Chair-local/TeachingReports/'):
    """load all excel summaries of evaluations.

    Parameters
    ----------
    path : string
        path to directory containing all strings (must include end slash)
        default: `/Users/jslater/Documents/Admin/Chair-local/TeachingReports/`

    """
    filenames = os.listdir(path)
    if path[-1] is not '/':
        path += '/'
    newlist = list([])
    first = True
    for i, filename in enumerate(filenames):
        if ('20' in filename and
            'xlsx' in filename and
            'coursestaught' in filename and
                '~' not in filename):
            newlist.append(path + filename)
            print('loading ', path + filename)
            db_new = load_evals(path + filename)
            print(db_new.shape)

            if first is True:
                combined = db_new
                first = False
            else:
                combined = append(combined, db_new)

    writer = pd.ExcelWriter(path + 'Combined_Evaluations.xlsx')
    combined.to_excel(writer, 'Sheet1')
    writer.save()
    return combined
