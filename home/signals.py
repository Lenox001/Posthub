from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Blog, Comment, Reply, Like, AuthorProfile, Category, Tag
from django.contrib.auth.models import User

# Signal to send an email when a new blog is created
@receiver(post_save, sender=Blog)
def send_blog_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New Blog Created on PostHub: {instance.title}"
        message = (
            f"A new blog has been created by {instance.author.username}:\n\n"
            f"Title: {instance.title}\nContent Preview: {instance.body_content[:100]}...\n"
            f"View the blog: https://epoxy.pythonanywhere.com/blog/{instance.slug}"
        )
        admin_email = 'epoxypython@gmail.com'
        send_mail(subject, message, None, [admin_email])

# Signal to send an email when a new comment is added
@receiver(post_save, sender=Comment)
def send_comment_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New Comment on Blog: {instance.blog.title}"
        message = (
            f"A new comment has been posted on the blog '{instance.blog.title}' by {instance.author.username}.\n\n"
            f"Comment: {instance.content[:100]}...\n"
            f"View the comment: https://epoxy.pythonanywhere.com/blog/{instance.blog.slug}"
        )
        admin_email = 'epoxypython@gmail.com'
        send_mail(subject, message, None, [admin_email])

# Signal to send an email when a reply is added to a comment
@receiver(post_save, sender=Reply)
def send_reply_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New Reply on Blog: {instance.comment.blog.title}"
        message = (
            f"A new reply has been posted on the comment of the blog '{instance.comment.blog.title}' by {instance.author.username}.\n\n"
            f"Reply: {instance.content[:100]}...\n"
            f"View the reply: https://epoxy.pythonanywhere.com/blog/{instance.comment.blog.slug}"
        )
        admin_email = 'epoxypython@gmail.com'
        send_mail(subject, message, None, [admin_email])

# Signal to handle user profile creation and send welcome email
@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    if created:
        # Create user profile
        AuthorProfile.objects.create(user=instance)
        # Send welcome email
        if instance.email:
            subject = "Welcome to PostHub!"
            message = (
                f"Hi {instance.username},\n\n"
                "Welcome to PostHub! We're excited to have you join our blogging community. Start exploring and sharing your stories today!"
            )
            send_mail(subject, message, None, [instance.email])

        # Send admin notification
        subject_admin = f"New User Signed Up on PostHub: {instance.username}"
        message_admin = (
            f"A new user has signed up on PostHub.\n\n"
            f"Username: {instance.username}\nEmail: {instance.email}\n"
            f"Check the admin panel for more details."
        )
        admin_email = 'epoxypython@gmail.com'
        send_mail(subject_admin, message_admin, None, [admin_email])

# Signal to send an email when a blog is liked
@receiver(post_save, sender=Like)
def send_blog_like_email(sender, instance, created, **kwargs):
    if created:
        subject = f"{instance.user.username} liked your blog on PostHub"
        message = f"Your blog '{instance.blog.title}' has been liked by {instance.user.username}."
        blog_author_email = instance.blog.author.email
        if blog_author_email:
            send_mail(subject, message, None, [blog_author_email])

# Signal to send email when a category or tag is created
@receiver(post_save, sender=Category)
@receiver(post_save, sender=Tag)
def send_category_or_tag_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New {instance.__class__.__name__} Created on PostHub"
        message = f"A new {instance.__class__.__name__} has been created: {instance.name}."
        admin_email = 'epoxypython@gmail.com'
        send_mail(subject, message, None, [admin_email])

# Signal to send email when a blog is deleted
@receiver(pre_delete, sender=Blog)
def send_blog_deletion_email(sender, instance, **kwargs):
    subject = f"Blog Deleted on PostHub: {instance.title}"
    message = f"The blog titled '{instance.title}' has been deleted."
    admin_email = 'epoxypython@gmail.com'
    send_mail(subject, message, None, [admin_email])

# Signal to send email when a comment is deleted
@receiver(pre_delete, sender=Comment)
def send_comment_deletion_email(sender, instance, **kwargs):
    subject = f"Comment Deleted on Blog: {instance.blog.title}"
    message = f"A comment has been deleted on the blog '{instance.blog.title}'.\n\nComment: {instance.content[:100]}..."
    admin_email = 'epoxypython@gmail.com'
    send_mail(subject, message, None, [admin_email])

# Signal to send email when a reply is deleted
@receiver(pre_delete, sender=Reply)
def send_reply_deletion_email(sender, instance, **kwargs):
    subject = f"Reply Deleted on Blog: {instance.comment.blog.title}"
    message = f"A reply has been deleted on the blog '{instance.comment.blog.title}'.\n\nReply: {instance.content[:100]}..."
    admin_email = 'epoxypython@gmail.com'
    send_mail(subject, message, None, [admin_email])

# Notify the commenter when their comment receives a reply
@receiver(post_save, sender=Reply)
def notify_commenter_on_reply(sender, instance, created, **kwargs):
    if created and instance.comment.author.email:  # Ensure the commenter has an email
        subject = f"New Reply to Your Comment on '{instance.comment.blog.title}'"
        message = (
            f"{instance.author.username} has replied to your comment on the blog '{instance.comment.blog.title}'.\n\n"
            f"Reply: {instance.content[:100]}...\n\n"
            f"View it here: https://epoxy.pythonanywhere.com/blog/{instance.comment.blog.slug}"
        )
        send_mail(subject, message, None, [instance.comment.author.email])
