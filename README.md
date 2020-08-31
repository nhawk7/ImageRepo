To run locally:
```sh
git clone https://github.com/gurksohal/ImageRepo.git
``` 

To install all requirements
```ssh
pip install -r requirements.txt
```
To recreate database tables:
```python
from imagerepo import db
db.create_all()
```

# Routes
### "/"
```
Search box -> which fetches all of the uploaded images. (redirect to /user/<username>)
If accessed by a logged-in user, show all of the users uploaded images 
```
### "/user/[username]"
```
all of the uploaded images by the desired user
```
### "/register, /login and /logout"
```
User auth
```
### "/search"
```
Upload an image to find similar images among all the uploaded images.
```

### "/upload"
```
User must be signed in to access this page
Upload an image.
- If the image has already been uploaded by another user
    - add a reference of the image, rather than reuploading the image again
```


# TODO:
```
- Add functionality for deleting images
- Add tests
- Improve the time complexity of searching for similar images.
    - Currently, time complexity is linear
```
