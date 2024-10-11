from flask import request, jsonify
from app import app, db
from app.models import ImageMeta
from app.utils.some_utils import upload_file_to_s3
import jwt  
from functools import wraps
import os

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]
        try:
            
            decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            
            return f(decoded_token, *args, **kwargs)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({'message': 'Token is invalid or expired'}), 401
    return decorator

@app.route('/upload', methods=['POST'])
@token_required
def upload_image(decoded_token):
    files = request.files.getlist('images')  
    urls = []
    
    
    user_id = decoded_token.get('sub').get('id')  
    image_list = []

    for file in files:
        if file:
            
            url = upload_file_to_s3(file, os.getenv('AWS_S3_BUCKET_NAME'))
            if url:
                
                image_meta = ImageMeta(filename=file.filename, url=url, user_id=user_id)  
                db.session.add(image_meta)
                image_list.append(image_meta)

    db.session.commit()
    images = [{
        'id': image.id,
        'filename': image.filename,
        'url': image.url,
        'user_id': image.user_id,
        'upload_date': image.upload_date.isoformat()  
    } for image in image_list]
    return jsonify({'images': images}), 201


@app.route('/images', methods=['GET'])
@token_required
def get_images(decoded_token):
    
    user_id = request.args.get('user_id')
    
    
    if not user_id:
        return jsonify({'message': 'user_id is required in query parameters'}), 400

    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)  

    
    pagination = ImageMeta.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    
    
    images = pagination.items

    
    image_list = [{
        'id': image.id,
        'filename': image.filename,
        'url': image.url,
        'user_id': image.user_id,
        'upload_date': image.upload_date.isoformat()  
    } for image in images]

    
    return jsonify({
        'images': image_list,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    }), 200


@app.route('/delete_images', methods=['DELETE'])
@token_required
def delete_images(decoded_token):
    
    payload = request.get_json()

    
    if not payload or 'image_ids' not in payload:
        return jsonify({'message': 'image_ids are required in the payload'}), 400

    image_ids = payload['image_ids']

    
    if not isinstance(image_ids, list) or not all(isinstance(id, int) for id in image_ids):
        return jsonify({'message': 'image_ids must be a list of integers'}), 400

    
    images_to_delete = ImageMeta.query.filter(ImageMeta.id.in_(image_ids)).all()

    if not images_to_delete:
        return jsonify({'message': 'No images found for the provided ids'}), 404

    
    for image in images_to_delete:
        db.session.delete(image)

    db.session.commit()  

    return jsonify({'message': 'Images deleted successfully'}), 204
