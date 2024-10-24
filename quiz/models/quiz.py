from django.db import models 
from .custom_user import CustomUser 
from django.utils import timezone 


class CommonAbstract(models.Model):
    created_at = models.DateTimeField(editable=False, null=True, blank=True, verbose_name='Thời điểm tạo')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời điểm cập nhật')


    class Meta:
        ordering = ('-created_at',)
        abstract = True 


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super(CommonAbstract, self).save(*args, **kwargs)


class Exam(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=255, verbose_name='Tên bài kiểm tra')
    room_name = models.CharField(max_length=255, verbose_name='Tên phòng thi')
    start_time = models.DateTimeField(verbose_name='Thời gian bắt đầu')
    finish_time = models.DateTimeField(verbose_name='Thời gian kết thúc')
    time_todo = models.IntegerField(default=15, verbose_name='Thời gian làm bài (phút)')
    room_code = models.CharField(max_length=15, unique=True, verbose_name='Mã phòng thi')
    created_by = models.CharField(max_length=255, verbose_name='Người tạo')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'QL Bài kiểm tra'
        verbose_name_plural = 'QL Bài kiểm tra'
        db_table = 'exams'


    def __str__(self):
        return f"{self.id} - {self.title} - {self.room_code}"


class Question(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='Bài kiểm tra')
    question_text = models.CharField(max_length=255, verbose_name='Câu hỏi')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'QL Câu hỏi'
        verbose_name_plural = 'QL Câu hỏi'
        db_table = 'questions'


    def __str__(self):
        return f"{self.id} - {self.question_text}"


class Answer(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Câu hỏi')
    answer_text = models.CharField(max_length=255, verbose_name='Câu trả lời')
    is_correct = models.BooleanField(default=False, verbose_name='Câu trả lời đúng')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'QL Đáp án'
        verbose_name_plural = 'QL Đáp án'
        db_table = 'answers'

    
    def __str__(self):
        return f"{self.id} - {self.answer_text}"


class Result(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='Người thực hiện')
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, verbose_name='Bài thi')
    score = models.IntegerField(default=0, verbose_name='Điểm số')
    

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kết quả thi'
        verbose_name_plural = 'Kết quả thi'
        db_table = 'results'

    
    def __str__(self):
        return f"{self.id} - {self.user.username}"


class ResultDetail(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Bài kiểm tra')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, verbose_name='Đáp án lựa chọn')
    is_correct = models.BooleanField(default=False, verbose_name='Kết quả (Đ/S)')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kết quả câu hỏi'
        verbose_name_plural = 'Kết quả câu hỏi'
        db_table = 'result_details'

    
    def __str__(self):
        return f"{self.id} - {self.is_correct}"
    

    def save(self, *args, **kwargs):
        if self.answer.is_correct:
            self.is_correct = True 
        super(ResultDetail, self).save(*args, **kwargs)


