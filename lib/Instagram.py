import SocialMediaAccount


class Instagram(SocialMediaAccount):

    def __repr__(self):
        return f"<Instagram Account: {self.username}>"

    def validate_account(self):
        # TODO -- use Instagram API to validate account exists
        return



