
#
# All models of houdini template manager generated from
# NOTE: Legacy tables created in postgres sql and igrated using 
# python manage.py inspectdb > models.py
from django.db import models
# Create your models here.

class BundleTypes(models.Model):
    """
    "Templates" and "Node snippet"

    Args:
        models (Model): Model object inherited

    """
    bundle_type = models.CharField(unique=True, max_length=35)

    def __str__(self) -> str:
        return f"{self.bundle_type}"

    class Meta:
        managed = False
        db_table = 'bundle_types'



class Tags(models.Model):
    """
    Tags table having different tags. Unique tags. 
    """
    tag = models.CharField(unique=True, max_length=35)

    def __str__(self) -> str:
        return f"{self.tag}"

    class Meta:
        managed = False
        db_table = 'tags'


class Bundles(models.Model):
    """Master table model

    Bundles table maintains all the user registered bundle.
    As of this model is created from migrations
    m-to-m field for tags created manually
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    version = models.IntegerField()
    artist = models.CharField(max_length=100)
    file_path = models.CharField(max_length=100)
    file_type = models.CharField(max_length=10)
    frame_start = models.BigIntegerField(blank=True, null=True)
    frame_end = models.BigIntegerField(blank=True, null=True)
    img_path = models.CharField(max_length=300, blank=True, null=True)
    favorite = models.BooleanField()
    bundle_type = models.ForeignKey(BundleTypes, models.DO_NOTHING)
    bundle_list = models.ForeignKey('BundlesList', models.DO_NOTHING)
    category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)
    context = models.ForeignKey('Contexts', models.DO_NOTHING, blank=True, null=True)
    houdini_version = models.ForeignKey('Versions', models.DO_NOTHING)

    # Tag field created manually to create M-to-M relationship 
    # through model BundlesTag
    tag = models.ManyToManyField('Tags', through='BundlesTag')
    created_at = models.DateTimeField(blank=True, null=True)
    frame_count = models.BigIntegerField(blank=True, null=True)


    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = 'bundles'


class BundlesList(models.Model):
    """
    bundles list table

    A list of bundles exposed in this model
    """
    bundle = models.CharField(unique=True, max_length=25)

    def __str__(self):
        return f"{self.bundle}"
    
    class Meta:
        managed = False
        db_table = 'bundles_list'


class BundlesTag(models.Model):

    """Many-To-Many relationship table for bundles and tags"""

    bundle = models.ForeignKey(Bundles, models.DO_NOTHING)
    tag = models.ForeignKey('Tags', models.DO_NOTHING)

    def __str__(self):
        return f"{self.bundle} ({self.tag})"

    class Meta:
        managed = False
        db_table = 'bundles_tag'
        unique_together = (('bundle', 'tag'),)



class Categories(models.Model):
    """ Category table with list of category"""

    category = models.CharField(unique=True, max_length=35)

    def __str__(self):
        return f"{self.category}"

    class Meta:
        managed = False
        db_table = 'categories'


class Contexts(models.Model):
    """ context table with list of context"""

    context = models.CharField(unique=True, max_length=35)

    def __str__(self):
        return f"{self.context}"

    class Meta:
        managed = False
        db_table = 'contexts'


class Versions(models.Model):
    """ Versions table to maintain houdini versions"""

    version = models.CharField(unique=True, max_length=35)

    def __str__(self):
        return f"{self.version}"

    class Meta:
        managed = False
        db_table = 'versions'