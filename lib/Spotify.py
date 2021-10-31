import SocialMediaAccount


class Spotify(SocialMediaAccount):

    def __repr__(self):
        return f"<Spotify Account: {self.username}>"

    def validate_account(self):
        # TODO -- use Spotify API to validate account exists
        return



