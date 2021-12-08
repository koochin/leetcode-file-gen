import json
import sys
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
 
NAME      = 'Liam'
DATE      = datetime.now().strftime("%m-%d-%Y")
EXTENSION = '.py'

LEETCODE_URL     = 'https://leetcode.com'
LEETCODE_GRAPHQL = 'https://leetcode.com/graphql'
LEETCODE_API     = LEETCODE_URL + '/api/problems/all/'
PROBLEM_URL      = LEETCODE_URL + '/problems/'

# start of leetcode-file-gen.py

GEN_ALL_PROBLEMS = sys.argv[1] \
                   if len(sys.argv) >= 2 \
                   and sys.argv[1] == '--all' \
                   else None

r = requests.get(LEETCODE_API)
problems = json.loads(r.text)

d = dict() # map question_id to question__title_slug

N = 0
for q in problems['stat_status_pairs']:
    qid = q['stat']['question_id']
    qslug = q['stat']['question__title_slug']
    d[qid] = qslug
    N = max(N, len(str(qid)))

if GEN_ALL_PROBLEMS:
    file = 'all_problems.txt'
    try:
        f = open(file, 'w')
    except:
        sys.exit(f'error: could not create {file}')
    text = [str(number).rjust(N, '0') + " " + name for number, name in d.items()]
    text = sorted(text)
    f.write('\n'.join(text))
    f.close()
    sys.exit(f'generated list of all problems in {file}')

# referenced: https://stackoverflow.com/a/56610178
data = {"operationName":"questionData","variables":{"titleSlug":"two-sum"},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

# question number
number = int(sys.argv[1]) \
         if len(sys.argv) >= 2 \
         else None # error

if not number:
    sys.exit(f'error: please provide a question id')

# print(number)

data['variables']['titleSlug'] = d[number]

r = requests.post(LEETCODE_GRAPHQL, json = data).json()

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
# default: 'html.parser'
soup = bs(r['data']['question']['content'], 'lxml')
# question_as_line =  soup.get_text().replace('\n',' ')
question     = soup.get_text()
title        = r['data']['question']['title']
question_id  = r['data']['question']['questionId']
difficulty   = r['data']['question']['difficulty']
python_code  = r['data']['question']['codeSnippets'][3]['code'] # 3 is Python3
test_case    = r['data']['question']['sampleTestCase']
title_slug   = d[int(question_id)]
question_url = PROBLEM_URL + title_slug

print(title_slug)
print(question_url)

file = question_id.rjust(N, '0') + '_' + title_slug.replace('-', '_') + EXTENSION

try:
    f = open(file, 'w')
except:
    sys.exit(f'error: could not create {file}')

body = (
    "'''" + "\n"
    "Author: " + NAME + "\n"
    "Date: " + DATE + "\n\n"
    "" + question_url + "\n\n"
    "" + question_id + ". " + title + "\n"
    "Difficulty: " + difficulty + "\n\n"
    "" + question + "\n"
    "Test Case:\n\n"
    "" + test_case + "\n"
    "'''" + "\n\n"
    "" + python_code + "\n"
)

f.write(body)
f.close()

# end of leetcode-file-gen.py
