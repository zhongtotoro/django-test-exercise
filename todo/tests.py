from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from todo.models import Task

# Create your tests here.
class SimpleTest(TestCase):
    def test_sample1(self):
        self.assertEqual(1 + 2, 3)

class TaskModelTestCase(TestCase):
    def test_create_task1(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 
        23, 59, 59))
        task = Task(title='task1', due_at=due)
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task1')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)


    def test_create_task2(self):
            task = Task(title='task2')
            task.save()

            task = Task.objects.get(pk=task.pk)
            self.assertEqual(task.title, 'task2')
            self.assertFalse(task.completed)
            self.assertEqual(task.due_at, None)

    def test_is_overdue_future(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertFalse(task.is_overdue(current))

   
    def test_is_overdue_past(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0)) 
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertTrue(task.is_overdue(current))

    
    def test_is_overdue_none(self):
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        task = Task(title='task2')
        task.save()

        self.assertFalse(task.is_overdue(current))


# ファイルの一番上のほうにある import 文に「Client」を追加するか、新しく書きます
from django.test import TestCase, Client 
# （他のimport文はそのまま残しておいて大丈夫です！）

# --- 中略（今までのテストコード） ---

# ▼ ファイルの一番下に、新しく画面テスト用のクラスを追加！
class TodoViewTestCase(TestCase):
    # GETメソッド（画面を普通に開く処理）のテスト
    def test_index_get(self):
        # 画像のコードをここに書きます（インデントに気をつけて！）
        client = Client()
        response = client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        self.assertEqual(len(response.context['tasks']), 0)

    def test_index_post(self):
        client = Client()
        data = {'title': 'Test Task', 'due_at': '2024-06-30 23:59:59'}
        response = client.post('/', data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        self.assertEqual(len(response.context['tasks']), 1)