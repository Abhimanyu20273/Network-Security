html_text1 = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Text Page</title>
<style>
  body, html {
    margin: 0;
  }
  .header {
    text-align: center;
    font-family: 'Times New Roman';
    font-size: 4em;
    font-weight: bold;
    margin-bottom: 2em; 
  }
  .line {
    text-align: center;
    margin-top: 0;
    margin-bottom: 0;
    font-size: 2em;
    font-family: 'Helvetica';
  }
  .grades {
    text-align: left;
    margin-top: 0;
    margin-bottom: 0;
    font-size: 2em;
    font-family: 'Helvetica';
  }
</style>
</head>
<body>
"""

html_degree_title = """
<div class="header">Some Institute of Technology</div>
"""


html_text2 = """
<div class="line">This is to certify that </div>
<div class="line">{} roll number {}</div>
<div class="line">has been awarded the degree of Bachelor of Engineering in Computer Science</div>
<div class="line">on 31-May-2023.</div>
</body>
</html>
"""


html_grade_card_title = """
<div class="header">Grade Card</div>
"""

html_text3 = """
<div class="grades">Name: {}</div>
<div class="grades">Roll Number: {}</div>
<div class="grades">Subject 1: {}/100</div>
<div class="grades">Subject 2: {}/100</div>
<div class="grades">Subject 3: {}/100</div>
<div class="grades">Subject 4: {}/100</div>
<div class="grades">Subject 5: {}/100</div>
"""
