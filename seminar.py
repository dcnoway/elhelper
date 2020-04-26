#data struct
class Seminar(object):
    def __init__(self,subject='',title='',videoUrl='',homeworkUrl=''):
        self.subject = subject
        self.title = title
        self.videoUrl = videoUrl
        self.homeworkUrl = homeworkUrl