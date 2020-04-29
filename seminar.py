#data struct
class Seminar(object):
    def __init__(self,subject='',title='',videoUrl='',homeworkUrl='',homeworkName=''):
        self.subject = subject
        self.title = title
        self.videoUrl = videoUrl
        self.homeworkUrl = homeworkUrl
        self.homeworkName = homeworkName
        self.homeworkTaskSheet = ''
    
    def __str__(self):
        return '<Seminar object>subject=%s, title=%s, videoUrl=%s, HomeworkUrl=%s, HomeworkName=%s, HomeworkTaskSheet=%s>' \
            % (self.subject, self.title, self.videoUrl, self.homeworkUrl, self.homeworkName, self.homeworkTaskSheet)