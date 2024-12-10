from docx2python import docx2python
 
# extract docx content
doc_result = docx2python("D:/1998/GYC 0198-0413 Casa Dr Martin Villa/casa del Dr. Villa.doc")

print (doc_result.body)