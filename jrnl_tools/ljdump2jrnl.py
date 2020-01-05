import glob
import os
import xml.etree.ElementTree as ET

entries = glob.glob('/tmp/ljdump/cbanek/L-*')

for entry in entries:
  entry_name = os.path.basename(entry)
  print('Parsing ', entry_name)
  tree = ET.parse(entry)
  root = tree.getroot()
  time = root.find('eventtime').text

  subject_node = root.find('subject')
  if subject_node is not None:
    subject = subject_node.text
  else:
    subject = ''

  text = root.find('event').text

  commentfile = entry.replace('L', 'C')

  comment_block = ''

  try:
    comments = ET.parse(commentfile).getroot()
    for comment in comments.findall('comment'):
      comment_user_node = comment.find('user')
      if comment_user_node is None:
        comment_user = 'unknown'
      else:
        comment_user = comment_user_node.text
      comment_body = comment.find('body').text
      if comment_body is None:
        print(f'empty comment body in {commentfile}')
        comment_body = ''
      comment_block += f'Comment by {comment_user}:\n\n'
      comment_block += comment_body + '\n\n'
  except FileNotFoundError:
    pass

  with open('/tmp/md/' + entry_name, 'w') as f:
    print(time + ': ' + subject, file=f)
    print(text, file=f)
    print(comment_block, file=f)
