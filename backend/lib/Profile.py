import Spotify as spot, Instagram as insta, Phone as phone, Snapchat as snap, LinkedIn as li


class Profile:
    # abstract profiles
    def __init__(self):
        self._first_name = None
        self._last_name = None
        self._img = None
        self._snapchat = None
        self._instagram = None
        self._phone = None
        self._spotify = None
        self._facebook = None
        self._linkedin = None

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def first_name(self):
        return self.first_name

    @first_name.setter
    def first_name(self, name):
        self._first_name = name

    @property
    def last_name(self):
        return self.last_name

    @last_name.setter
    def last_name(self, name):
        self._last_name = name

    @property
    def img(self):
        if self._img is None:
            # TODO -- randomly generated avatar
            return 'hi'
        else:
            return self._img

    @img.setter
    def img(self, img_url):
        # TODO -- validate valid image
        self._img = img_url

    @property
    def snap(self):
        return snap.Snapchat(self._snapchat)

    @snap.setter
    def snap(self, snapchat_username):
        # TODO -- validate snap username
        # https://stories.mlh.io/authenticate-your-users-with-snapchats-login-kit-a54a7f09e2a3
        self._snapchat = snapchat_username

    @property
    def insta(self):
        return insta.Instagram(self._instagram)

    @insta.setter
    def insta(self, insta_username):
        # TODO -- validate insta username
        # https://developers.facebook.com/docs/instagram-basic-display-api/getting-started
        self._instagram = insta_username

    @property
    def phone(self):
        return phone.Phone(self._phone)

    @phone.setter
    def phone(self, number):
        # TODO -- validate phone number
        # https://stackabuse.com/validating-and-formatting-phone-numbers-in-python/
        # https://dev.to/mraza007/sending-sms-using-python-jkd
        self._phone = number

    @property
    def spotify(self):
        return spot.Spotify(self._spotify)

    @spotify.setter
    def spotify(self, username):
        # TODO -- validate spotify user
        # https://medium.com/@sedwardscode/creating-a-spotify-app-on-the-spotify-developer-page-16907b5872e8
        self._phone = username

    @property
    def facebook(self):
        return fb.Facebook(self._facebook)

    @facebook.setter
    def facebook(self, username):
        # TODO -- validate spotify user
        self._facebook = username

    @property
    def linkedin(self):
        return li.LinkedIn(self._linkedin)

    @linkedin.setter
    def linkedin(self, username):
        # TODO -- validate spotify user
        self._linkedin = username
