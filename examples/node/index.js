const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');
const process = require('process');

function getUniqueId() {
   var result           = '';
   var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < 32; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}


function runVerification(target, jsonObj, enrollmentPathsArray, verificationPath, callback) {

  const form = new FormData();
  form.append('json', JSON.stringify(jsonObj));

  for (let i = 0; i < enrollmentPathsArray.length; i++) {
    form.append(jsonObj.enrollmentsFileKeys[i], fs.createReadStream(enrollmentPathsArray[i]), {
      filename: path.basename(enrollmentPathsArray[i]),
    });
  }

  form.append(jsonObj.verificationFileKey, fs.createReadStream(verificationPath), {
    filename: path.basename(verificationPath),
  });

  axios.post(`https://alpha-siamese.voiceit.io/${target}`, form, {
    headers: form.getHeaders(),
  }).then((httpResponse) => {
    callback(httpResponse.data);
  }).catch((error) => {
    callback(error.response.data);
  });

}




const jsonObj = {
  enrollmentsFileKeys: [
      'enrollment1FileKey',
      'enrollment2FileKey',
      'enrollment3FileKey',
  ],
  verificationFileKey: 'verificationFileKey',
  uniqueId: getUniqueId(),
};


if (process.argv.length !== 3) {
  console.log('Please pass the target (either "siv3" or "siv4") after the command "node index.js"\n');
  console.log('Usage: node index.js [siv3|siv4]');
  process.exit()
}

const target = process.argv[2];

if (target !== 'siv3' && target !== 'siv4') {
  console.log('The target argument must be either "siv3" or "siv4"\n');
  process.exit()
}


let enrollmentPathsArray = ['../../files/' + target + '/enrollmentA1.wav', '../../files/' + target + '/enrollmentA2.wav', '../../files/' + target + '/enrollmentA3.wav'];
let verificationPath = '../../files/' + target + '/verificationA.wav';
jsonObj.uniqueId = getUniqueId();
runVerification(target, jsonObj, enrollmentPathsArray, verificationPath, (jsonResponse) => {
  console.log('Running user A enrollment files against user A verification file')
  console.log(jsonResponse);
  console.log();
})

enrollmentPathsArray = ['../../files/' + target + '/enrollmentA1.wav', '../../files/' + target + '/enrollmentA2.wav', '../../files/' + target + '/enrollmentA3.wav'];
verificationPath = '../../files/' + target + '/verificationB.wav';
jsonObj.uniqueId = getUniqueId();
runVerification(target, jsonObj, enrollmentPathsArray, verificationPath, (jsonResponse) => {
  console.log('Running user A enrollment files against user B verification file')
  console.log(jsonResponse);
  console.log();
})

enrollmentPathsArray = ['../../files/' + target + '/enrollmentB1.wav', '../../files/' + target + '/enrollmentB2.wav', '../../files/' + target + '/enrollmentB3.wav'];
verificationPath = '../../files/' + target + '/verificationB.wav';
jsonObj.uniqueId = getUniqueId();
runVerification(target, jsonObj, enrollmentPathsArray, verificationPath, (jsonResponse) => {
  console.log('Running user B enrollment files against user B verification file')
  console.log(jsonResponse);
  console.log();
})

enrollmentPathsArray = ['../../files/' + target + '/enrollmentB1.wav', '../../files/' + target + '/enrollmentB2.wav', '../../files/' + target + '/enrollmentB3.wav'];
verificationPath = '../../files/' + target + '/verificationA.wav';
jsonObj.uniqueId = getUniqueId();
runVerification(target, jsonObj, enrollmentPathsArray, verificationPath, (jsonResponse) => {
  console.log('Running user B enrollment files against user A verification file')
  console.log(jsonResponse);
  console.log();
})
