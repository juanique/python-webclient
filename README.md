#### Examples

### Github

This is how you would add a new key to your github account

    from webclient import WebClient

    # The public key should be here
    key = 'ssh-rs AAA.....user@ubuntu'

    data = {
        'title' : "My awesome key"
        'key' : key
    }
    client = WebClient("https://api.github.com")
    client.authenticate(username="gituser", password="gitpassword")
    client.post("/user/keys", data)

### Facebook

You may want to extend the client to set default headers or parameters

    from webclient import WebClient

    class Facebook(WebClient):

        def __init__(self, access_token=None, verbose=False):
            self.access_token = access_token
            self.fb_host = "https://graph.facebook.com"
            super(Facebook, self).__init__(self.fb_host, verbose=verbose)

        def get(self, *args, **kwargs):
            data = kwargs.get('data', {})
            data['access_token'] = self.access_token
            kwargs['data'] = data
            return super(Facebook, self).get(*args, **kwargs).data

        def post(self, path, *args, **kwargs):
            path = "%s?access_token=%s" % (path, self.access_token)
            kwargs['content_type'] = 'multipart/form-data'
            return super(Facebook, self).post(path, *args, **kwargs).data

And later use it it like this

    fb = Facebook(access_token="...")

    # get the user information
    fb.get("/me").data

    # post a picture to the default app album
    fb.post("/me/photos", data={"message": "Awesome description"},
        files={"image": "/home/user/awesome.jpg"})
