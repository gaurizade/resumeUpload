import os
import json
import logging
import ntpath
import datetime
import tempfile
import asyncio
from pathlib import Path
import configuration
import resumeparser
import conf
import azure.functions as func
from azure.storage.blob import BlockBlobService
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    resume = req.params.get('filename')
    is_local = None
    if not resume:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            pass

    if resume:
        storage_acc = None
        storage_acc_key = None
        container_name = None
        connection_strings = None
        file_path = None
        extracted_data = {}
        filename = ntpath.basename(resume)
        file_name_without_ext = Path(filename).stem
        config_obj = configuration.Configuration()
        file_exists = True
        log_file_name = ''
        try:
            log_file_name = file_name_without_ext + "_" + \
                str(datetime.now().strftime(
                    config_obj.strings.dt_format_log)) + ".log"
        except:
            logging.warning("Couldn't get log details from config")
        if is_local:
            file_path = resume
            log_folder_path = os.path.join(os.path.dirname(resume), "logs")
            if not os.path.exists(log_folder_path):
                os.makedirs(log_folder_path)
            log_file_path = os.path.join(log_folder_path, log_file_name)
        else:
            temp_file_path = tempfile.gettempdir()
            blob_name = os.path.basename(resume)
            file_path = os.path.join(temp_file_path, blob_name)
            log_file_path = os.path.join(temp_file_path, log_file_name)
            try:
                storage_acc = conf.storage_account
                storage_acc_key = conf.storage_account_key
                container_name = conf.container_name
                container_logs = conf.container_log
                connection_strings = conf.connection_string
            except:
                # logging.error("Couldn't get blob details from conf")
                pass
            try:
                block_blob_service = BlockBlobService(
                    storage_acc, storage_acc_key, connection_string=connection_strings)
                block_blob_service.get_blob_to_path(
                    container_name, blob_name, file_path)
            except Exception as ex:
                logging.exception(str(ex))
                file_exists = False
                logging.exception(
                    "Could not fetch resume file from blob path.")

        logging.getLogger("pdfminer").setLevel(logging.WARNING)
        cusom_log = logging.getLogger(file_name_without_ext)

        if file_exists:
            res_ext_obj = resumeparser.ResumeParser(file_path)
            try:
                check_file_exists = Path(file_path)
                if check_file_exists.is_file():
                    extracted_data = res_ext_obj.get_extracted_data()
                else:
                    logging.error("File not found in speciied path")
            except Exception as ex:
                logging.error(str(ex))
                logging.error("Error in resume parser")
        if not is_local:
            try:
                block_blob_service = BlockBlobService(
                    storage_acc, storage_acc_key)
                block_blob_service.create_blob_from_path(
                    container_logs, log_file_name, log_file_path)
            except Exception as ex:
                # logging.exception(str(ex))
                logging.exception("Failed logging to blob.")

        data = json.dumps(extracted_data)
        return func.HttpResponse(data)
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass filename in the query string or in the request body for a personalized response.",
            status_code=200)
