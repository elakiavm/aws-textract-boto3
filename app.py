'''
Created on 

Course work: 
    AWS-textract

@author: Elakia

Source:

'''
import boto3
from trp import Document


#1. PLAINTEXT detection from documents:
def plain_text(textractmodule,s3BucketName,PlaindocumentName):
    response = textractmodule.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': PlaindocumentName
            }
        })
    print ('------------- Print Plaintext detected text ------------------------------')
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print (item["Text"])
    return 

def form(textractmodule,s3BucketName,FormdocumentName):
#2. FORM detection from documents:
    response = textractmodule.analyze_document(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': FormdocumentName
            }
        },
        FeatureTypes=["FORMS"])
    doc = Document(response)
    print ('------------- Print Form detected text ------------------------------')
    for page in doc.pages:
        for field in page.form.fields:
            print("Key: {}, Value: {}".format(field.key, field.value))
    return


def table(textractmodule,s3BucketName,TabledocumentName):
    #2. TABLE data detection from documents:
    response = textractmodule.analyze_document(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': TabledocumentName
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
    PlaindocumentName = "Screenshot from 2022-08-07 08-30-59.png"
    FormdocumentName = "test.jpg"
    TabledocumentName = "Screenshot from 2022-08-07 09-22-02.png"

    # Amazon Textract client
    textractmodule = boto3.client('textract')

    # plain_text(textractmodule,s3BucketName,PlaindocumentName)
    form(textractmodule,s3BucketName,FormdocumentName)
    # table(textractmodule,s3BucketName,TabledocumentName)

    pass


if __name__ == '__main__':
    startpy()
