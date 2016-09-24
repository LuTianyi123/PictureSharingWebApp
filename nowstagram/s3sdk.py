# -*- encoding: UTF-8 -*-

from nowstagram import app
import boto
import boto.s3.connection
from boto.s3.key import Key

access_key = 'put your access key here!'
secret_key = 'put your secret key here!'

conn = boto.connect_s3(aws_access_key_id = access_key,aws_secret_access_key = secret_key)

bucket_name = app.config['S3_BUCKET_NAME']
bucket = conn.get_bucket(bucket_name)

## test connection
for buc in conn.get_all_buckets():
        print buc.name

k = Key(bucket)

def s3_upload_file(source_file, save_file_name):
        k.key = save_file_name
        k.set_contents_from_file(source_file)
        k.set_canned_acl('public-read')
        file_url = k.generate_url(0, query_auth=False, force_http=True)
        return file_url
