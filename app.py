'''
Created on 

Course work: 
    AWS-textract

@author: Elakia

Source:

'''
import boto3
from trp import Document


#1. plaintextimage detection from documents:
def plain_text(textractmodule,s3BucketName,plaintextimage):
    response = textractmodule.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': plaintextimage
            }
        })
    print ('------------- Print plaintextimage detected text ------------------------------')
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print (item["Text"])
    return 

def form(textractmodule,s3BucketName,formimage):
#2. FORM detection from documents:
    response = textractmodule.analyze_document(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': formimage
            }
        },
        FeatureTypes=["FORMS"])
    doc = Document(response)
    print ('------------- Print Form detected text ------------------------------')
    for page in doc.pages:
        for field in page.form.fields:
            print("Key: {}, Value: {}".format(field.key, field.value))
    return


def table(textractmodule,s3BucketName,tableimage):
    #2. TABLE data detection from documents:
    response = textractmodule.analyze_document(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': tableimage
            }
        },
        FeatureTypes=["TABLES"])
    doc = Document(response)

    print ('------------- Print Table detected text ------------------------------')
    for page in doc.pages:
        for table in page.tables:
            for r, row in enumerate(table.rows):
                itemName  = ""
                for c, cell in enumerate(row.cells):
                    print("Table[{}][{}] = {}".format(r, c, cell.text))
    return

def startpy():
    # S3 Bucket Data
    s3BucketName = "textractfrp"
    plaintextimage = "Screenshot from 2022-08-07 08-30-59.png"
    formimage = "test.jpg"
    tableimage = "Screenshot from 2022-08-07 09-22-02.png"

    # Amazon Textract client
    textractmodule = boto3.client('textract')

    plain_text(textractmodule,s3BucketName,plaintextimage)
    form(textractmodule,s3BucketName,formimage)
    table(textractmodule,s3BucketName,tableimage)

    pass


if __name__ == '__main__':
    startpy()
