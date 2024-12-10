cd /home/vlab/PycharmProjects/TestlinkAPI


#run below command to install the required libraries
#pip install -r Utils/Libraries/requirements.txt 

python3 -m Core.Creations.create_test_pro
python3 -m Utils.Excel_to_XML.Keywords
python3 -m Utils.Excel_to_XML.Req_Spec
python3 -m Core.Upload_XML_files.upload_xml_files
python3 -m Core.Creations.import_TestCases
python3 -m Core.Add_test_cases.add_TC_to_plan
python3 -m Core.Requirement_addition.assign_requirements


#if the project is already existing and youwant to delete it run below command
#python3 -m Core.Deletions.delete_test_project
