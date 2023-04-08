import smtpd
import asyncore
from datetime import datetime
import email
import os
import face_recognition
from email.mime.text import MIMEText


class CustomSMTPServer(smtpd.SMTPServer):
    no = 0
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options= None, rcpt_options = None):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        # print(type(data['from']))  
        filename_eml = 'request.eml'
        f = open(filename_eml, 'wb')
        f.write(data)
        f.close      
        self.no += 1
        msg = email.message_from_file(open(filename_eml))
        # Create file structure.
        filepath_pic = 'images/'
        filepath_eml = 'emls/' 
        filepath_Call_pics = 'image_database'
        os.makedirs(filepath_pic, exist_ok=True)
        os.makedirs(filepath_eml, exist_ok=True)
        os.makedirs(filepath_Call_pics, exist_ok=True)
        
        for part in msg.walk():
            print(part.get_content_type())
            if part.get_content_type() == 'application/octet-stream':
                image_data = part.get_payload(decode=True)
                # Save the image to a file
                request_img = 'request.jpg'
                output_call_picpath = os.path.join(filepath_Call_pics,request_img)
                with open(output_call_picpath, 'wb') as f:
                    f.write(image_data)
                    f.close
                print('True')
                
                image_data = part.get_payload(decode=True)
                # Load the jpg files into numpy arrays
                biden_image = face_recognition.load_image_file(os.path.join(filepath_Call_pics,"request.jpg"))
                obama_image = face_recognition.load_image_file(os.path.join(filepath_Call_pics,"ru3.png"))
                unknown_image = face_recognition.load_image_file(output_call_picpath)
                
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                
                # Get the face encodings for each face in each image file
                # Since there could be more than one face in each image, it returns a list of encodings.
                # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
                try:
                    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
                    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
                    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
                except IndexError:
                    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
                    # quit()

                known_faces = [
                    biden_face_encoding,
                    obama_face_encoding
                ]

                # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
                results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
                if format(results[0]) == 'True':
                    print("I know this man. This man is Sonya.")
                else:
                    print("I don't know.")
                    
                    with open('request.eml', 'r') as f:
                        eml = email.message_from_file(f)
                    updated_pic_filename = '%s-%s.jpg' % (eml['From'],datetime.now().strftime('%Y%m%d%H%M%S'))
                    updated_eml_filename = '%s-%s.eml' % (eml['From'],datetime.now().strftime('%Y%m%d%H%M%S'))
                    
                    
                    updated_eml = MIMEText('Updated_eml')
                    updated_person = eml['person']
                    updated_image = eml['image']
                    # add the headers from the original EML
                    del eml['person'] , eml['image']
                    
                    for par in eml.walk():
                        if par.get_content_type() == 'application/octet-stream':
                            del par['Content-Disposition']
                            par['Content-Disposition'] = 'attachment; filename=%s'% (updated_pic_filename)
                            print(par['Content-Disposition'])
                    updated_eml = eml
                    updated_eml['person'] = 'Unknown'
                    updated_eml['image'] = updated_pic_filename       
                    print('Saved this man eml and jpg file.')
                    # save the updated EML to a file
                    output_path_eml = os.path.join(filepath_eml,updated_eml_filename)
                    with open(output_path_eml, 'w') as fe:
                        fe.write(updated_eml.as_string())  
                        fe.close                   
                    # save the updated jpg to a file
                    output_path_pic = os.path.join(filepath_pic,updated_pic_filename)
                    with open(output_path_pic, 'wb') as fp:
                        fp.write(image_data)
                        fp.close                  
                                        
server = CustomSMTPServer(('192.168.104.11', 1025),None)

asyncore.loop()