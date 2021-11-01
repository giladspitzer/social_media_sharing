import SocialMediaAccount


class Snapchat(SocialMediaAccount):

    def __repr__(self):
        return f"<Snapchat Account: {self.username}>"

    def validate_account(self):
        # TODO -- use Snap API to validate account exists
        return



