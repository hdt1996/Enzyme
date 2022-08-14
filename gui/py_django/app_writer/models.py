# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CssAnimatable(models.Model):
    section = models.TextField(db_column='Section', blank=True, null=True)  # Field name made lowercase.
    opera = models.CharField(db_column='Opera', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    chrome = models.CharField(db_column='Chrome', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    edge = models.CharField(db_column='Edge', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    firefox = models.CharField(db_column='FireFox', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    safari = models.CharField(db_column='Safari', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    property = models.CharField(db_column='Property', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.property}"
    class Meta:
        db_table = 'CSS Animatable'
        verbose_name_plural = db_table


class CssBrowserSupport(models.Model):
    property = models.TextField(db_column='Property', blank=True, null=True)  # Field name made lowercase.
    edge = models.CharField(db_column='Edge', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    firefox = models.CharField(db_column='Firefox', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    chrome = models.CharField(db_column='Chrome', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    safari = models.CharField(db_column='Safari', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    opera = models.CharField(db_column='Opera', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.property}"
    class Meta:
        
        db_table = 'CSS Browser Support'
        verbose_name_plural = db_table

class CssDefaultValues(models.Model):
    element = models.TextField(db_column='Element', blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.element}"
    class Meta:
        
        db_table = 'CSS Default Values'
        verbose_name_plural = db_table

class CssEntities(models.Model):
    value = models.TextField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    char = models.CharField(db_column='Char', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.char}"
    class Meta:
        
        db_table = 'CSS Entities'
        verbose_name_plural = db_table

class CssFallbackFonts(models.Model):
    font_family = models.TextField(db_column='Font_Family', blank=True, null=True)  # Field name made lowercase.
    example_text = models.CharField(db_column='Example_Text', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.font_family}"
    class Meta:
        
        db_table = 'CSS Fallback Fonts'
        verbose_name_plural = db_table

class CssFunctions(models.Model):
    function = models.TextField(db_column='Function', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.function}"
    class Meta:
        
        db_table = 'CSS Functions'
        verbose_name_plural = db_table

class CssPxEmConverter(models.Model):
    px = models.TextField(db_column='Px', blank=True, null=True)  # Field name made lowercase.
    em = models.CharField(db_column='Em', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    percent = models.CharField(db_column='Percent', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.px}"
    class Meta:
        
        db_table = 'CSS PX-EM Converter'
        verbose_name_plural = db_table

class CssReference(models.Model):
    value = models.TextField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.value}"
    class Meta:
        
        db_table = 'CSS Reference'
        verbose_name_plural = db_table

class CssReferenceAural(models.Model):
    value = models.TextField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    property = models.CharField(db_column='Property', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    css = models.CharField(db_column='Css', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.property}"
    class Meta:
        
        db_table = 'CSS Reference Aural'
        verbose_name_plural = db_table

class CssSelectors(models.Model):
    selector = models.TextField(db_column='Selector', blank=True, null=True)  # Field name made lowercase.
    example = models.CharField(db_column='Example', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    example_description = models.CharField(db_column='Example_Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.selector}"
    class Meta:
        
        db_table = 'CSS Selectors'
        verbose_name_plural = db_table

class CssUnits(models.Model):
    unit = models.TextField(db_column='Unit', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    edge = models.CharField(db_column='Edge', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    chrome = models.CharField(db_column='Chrome', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    firefox = models.CharField(db_column='FireFox', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    safari = models.CharField(db_column='Safari', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    opera = models.CharField(db_column='Opera', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.unit}"
    class Meta:
        
        db_table = 'CSS Units'
        verbose_name_plural = db_table

class CssProperties(models.Model):
    section = models.TextField(db_column='Section', blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    property = models.CharField(db_column='Property', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    chrome = models.CharField(db_column='Chrome', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    edge = models.CharField(db_column='Edge', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    firefox = models.CharField(db_column='FireFox', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    safari = models.CharField(db_column='Safari', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    opera = models.CharField(db_column='Opera', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    css = models.CharField(db_column='Css', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    example = models.CharField(db_column='Example', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return f"{self.id} - {self.section}"
    class Meta:
        
        db_table = 'CSS_Properties'
        verbose_name_plural = db_table