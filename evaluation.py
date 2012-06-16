#### evaluation.py
#
# Evaluates the performance of the mini_qa question-answering system.

#### Library imports

import mini_qa

# Standard library
import json

class QAPair():
    """
    Stores a question and a list of acceptable answers.
    """
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers

def main():
    qa_pairs = load_qa_pairs()
    perfect_answers = 0
    okay_answers = 0
    rank_sum = 0
    num_questions = len(qa_pairs)
    print "Generating candidate answers for %s questions" % num_questions
    for (j, qa_pair) in enumerate(qa_pairs):
        print "Processing question %s" % j
        cr = correct_results(answers(qa_pair.question), qa_pair.answers)
        if 0 in cr:
            perfect_answers += 1
        if len(cr) > 0:
             okay_answers += 1
             rank_sum += cr[0]
    print "{} of {} had a correct answer in the top 20 ({:.2%})".format(
        okay_answers, num_questions, float(okay_answers) / num_questions)
    print "Average rank for answers in the top 20: {:.2f}".format(
        float(rank_sum) / okay_answers)
    print "{} returned a perfect answer ({:2%})".format(
        perfect_answers, float(perfect_answers) / num_questions)

def load_qa_pairs():
    """
    Return a list of QAPair instances, loaded from the file
    qa_pairs.json.
    """
    f = open("qa_pairs.json")
    qa_pairs = json.load(f)
    f.close()
    return [QAPair(qa_pair["question"], qa_pair["answers"]) 
            for qa_pair in qa_pairs]

def answers(question):
    """
    Return a list of the top 20 answers generated by `mini_qa.qa` to
    `question`.  Note that the standard format for those answers is as
    tuple (representeting an n-gram), and so we join the tuple
    elements around spaces.
    """
    return [" ".join(answer) 
            for (answer, score) in mini_qa.qa(question)[:20]]

def correct_results(candidate_answers, acceptable_answers):
    """
    Return a list containing the ranking of all elements of the list
    `candidate_answers` which are also in the list of
    `acceptable_answers`.
    """
    return [j for (j, answer) in enumerate(acceptable_answers)
            if answer in correct_answers]

if __name__ == "__main__":
    main()