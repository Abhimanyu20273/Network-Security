from flask import Flask, jsonify, request, send_from_directory, make_response, abort
from flask_cors import CORS
from PyPDF4 import PdfFileReader
from pdf_generator import create_pdf
from hash import generate_signature
from students import get_student_data

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'


@app.route('/get_document', methods=['GET'])
def get_document():
    name = request.args.get('name',None)
    rollNum = request.args.get('roll_num','')
    aadharLast4Digits = request.args.get('aadhar_last_4_digits','')
    docType = request.args.get('doc_type','Degree')
    print(f'name=<{name}>, rollNum=<{rollNum}>, aadharLast4Digits=<{aadharLast4Digits}>,docType=<{docType}>')

    studentData = get_student_data(name, rollNum, aadharLast4Digits)
    if not studentData:
        response = make_response('No such record found', 404)
        return response

    pdfFile = create_pdf(studentData, docType)
    registrarSignature = generate_signature(pdfFile)
    directorSignature = generate_signature(pdfFile,registrarSignature)

    response = make_response(send_from_directory(directory='./', path=pdfFile, as_attachment=True))
    response.headers['Signature1'] = registrarSignature
    response.headers['Signature2'] = directorSignature
    response.headers['fileName'] = pdfFile.split('/')[-1]
    return response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Expose-Headers', 'Signature1, Signature2, fileName')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow all domains
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
