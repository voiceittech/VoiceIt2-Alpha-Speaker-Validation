import json
import random
import requests
import string
import argparse
import sys


def randomString(stringLength=32):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def runVerification(enrollmentPaths, verificationPath, target):

    #  These will be passed in both the JSON multipart text fields
    # as well as as the keys for the multipart form file keys
    enrollment1FileKey = 'enrollment1'
    enrollment2FileKey = 'enrollment2'
    enrollment3FileKey = 'enrollment3'
    verificationFileKey = 'verification'

    #  Create multipart text field with the key 'json'
    jsonObj = {
        'json':  json.dumps(
            {
                'enrollmentsFileKeys': [
                    enrollment1FileKey,
                    enrollment2FileKey,
                    enrollment3FileKey,
                ],
                'verificationFileKey': verificationFileKey,
                'uniqueId': randomString(),
            }
        ),
    }

    try:
        #  Open all files that need to be used (caught in IOError...)
        enrollmentFile1 = open(enrollmentPaths[0], 'rb')
        enrollmentFile2 = open(enrollmentPaths[1], 'rb')
        enrollmentFile3 = open(enrollmentPaths[2], 'rb')
        verificationFile = open(verificationPath, 'rb')

        #  (string.replace() used to strip path from filename)
        filesObj = [

            (enrollment1FileKey,
             (enrollmentPaths[0].replace('./files/' + target + '/', ''),
              enrollmentFile1,
              'this mime is not used')),

            (enrollment2FileKey,
             (enrollmentPaths[1].replace('./files/' + target + '/', ''),
              enrollmentFile2,
              'this mime is not used')),

            (enrollment3FileKey,
             (enrollmentPaths[2].replace('./files/' + target + '/', ''),
              enrollmentFile3,
              'this mime is not used')),

            (verificationFileKey,
             (verificationPath.replace('./files/' + target + '/', ''),
              verificationFile,
              'this mime is not used')),
        ]

        #  Caught in requests.exceptions.HTTPError as e...
        response = requests.post('https://alpha-siamese.voiceit.io/' + target,
                                 data=jsonObj,
                                 files=filesObj
                                 )

        enrollmentFile1.close()
        enrollmentFile2.close()
        enrollmentFile3.close()
        verificationFile.close()
        print('response: ', response.json())
    except requests.exceptions.HTTPError as e:
        enrollmentFile1.close()
        enrollmentFile2.close()
        enrollmentFile3.close()
        verificationFile.close()
        print('exception: ', e.read())
    except IOError as e:
        enrollmentFile1.close()
        enrollmentFile2.close()
        enrollmentFile3.close()
        verificationFile.close()
        print('exception: ', e.read())


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", help="target: [ siv3 | siv4 ]")
    args = parser.parse_args()

    if args.target is None:
        parser.print_help()
        sys.exit(1)

    #  check value of target
    if args.target != 'siv3' and args.target != 'siv4':
        print('target must be of the following: [ siv3 | siv4 ]')
        sys.exit(1)

    print('Running user A enrollment files against user A verification file')
    runVerification(
        ['./files/' + args.target + '/enrollmentA1.wav',
         './files/' + args.target + '/enrollmentA2.wav',
         './files/' + args.target + '/enrollmentA3.wav'],
        './files/' + args.target + '/verificationA.wav',
        args.target)

    print('Running user A enrollment files against user B verification file')
    runVerification(
        ['./files/' + args.target + '/enrollmentA1.wav',
         './files/' + args.target + '/enrollmentA2.wav',
         './files/' + args.target + '/enrollmentA3.wav'],
        './files/' + args.target + '/verificationB.wav',
        args.target)

    print('Running user B enrollment files against user B verification file')
    runVerification(
        ['./files/' + args.target + '/enrollmentB1.wav',
         './files/' + args.target + '/enrollmentB2.wav',
         './files/' + args.target + '/enrollmentB3.wav'],
        './files/' + args.target + '/verificationB.wav',
        args.target)

    print('Running user B enrollment files against user A verification file')
    runVerification(
        ['./files/' + args.target + '/enrollmentB1.wav',
         './files/' + args.target + '/enrollmentB2.wav',
         './files/' + args.target + '/enrollmentB3.wav'],
        './files/' + args.target + '/verificationA.wav',
        args.target)
