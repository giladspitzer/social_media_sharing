import SocialMediaAccount


class Facebook(SocialMediaAccount):

    def __repr__(self):
        return f"<Facebook Account: {self.username}>"

    def validate_account(self):
        # TODO -- use FB API to validate account exists
        return



