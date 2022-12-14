.. _selectize:

================
Selectize Widget
================

Rendering choice fields using a ``<select>``-element becomes quite impractical when there are too
many options to select from. For this purpose, the Django admin backend offers so called
`auto complete fields`_, which loads a filtered set options from the server as soon as the user
starts typing into the input field. This widget is based on the Select2_ plugin, which itself
depends upon jQuery, and hence it is not suitable for **django-formset** which aims to be JavaScript
framework agnostic.

.. _auto complete fields: https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
.. _Select2: https://select2.org/


Usage with fixed Number of Choices
----------------------------------

Assume, we have an address form defining a ChoiceField_ to choose from a city. If this number of
cities exceeds say 25, we should consider to render the select box using the special widget
:class:`formset.widgets.Selectize`:

.. _ChoiceField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#django.forms.ChoiceField 

.. code-block:: python

	from django.forms import fields, forms, widgets
	from formset.widgets import Selectize

	class AddressForm(forms.Form):
	    # other fields

	    city = fields.ChoiceField(
	        choice=[(1, "London"), (2, "New York"), (3, "Tokyo"), (4, "Sidney"), (5, "Vienna")],
	        widget=Selectize,
	    )

This widget waits for the user to type some characters into the input field for city. If the entered
string matches the name of one or more cities (event partially), then a list of options is generated
containing the matching cities. By adding more characters to the input field, that list will shrink
to only a few or eventually no entry. This makes the selection simple and comfortable.


Usage with dynamic Number of Choices
------------------------------------

Sometimes we don't want to handle the choices using a static list. For instance, when we store them
in a Django model, we point a foreign key onto the chosen entry of that model. The above example
then can be rewritten by replacing the ChoiceField_ against a ModelChoiceField_. Instead of
``choices`` this field requires a ``queryset`` as parameter. For the form we defined above, we
use a Django model named ``Cities`` with ``name`` as identifier. All cities we can select from,
are now stored in a database table.

.. _ModelChoiceField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#django.forms.ModelChoiceField 

.. code-block:: python

	from django.forms import fields, forms, models, widgets
	from formset.widgets import Selectize

	class AddressForm(forms.Form):
	    # other fields

	    city = models.ModelChoiceField(
	        queryset=Cities.objects.all(),
	        widget=Selectize(
	            search_lookup='name__icontains',
	            placeholder="Choose a city",
	        ),
	    )

Here we instantiate the widget :class:`formset.widgets.Selectize` using the following parameters:

* ``search_lookup``: A Django `lookup expression`_. For choice fields with more than 50 options,
  this instructs the **django-formset**-library on how to look for other entries in the database. 
* ``placeholder``: The empty label shown in the select field, when no option is selected.
* ``attrs``: A Python dictionary of extra attributes to be added to the rendered ``<select>``
  element.

.. _lookup expression: https://docs.djangoproject.com/en/stable/ref/models/lookups/#lookup-reference


Endpoint for Dynamic Queries 
----------------------------

In contrast to other libraries offering autocomplete fields, such as `Django-Select2`_,
**django-formset** does not require to add an explicit endpoint to the URL routing. Instead it
shares the same endpoint for form submission as for querying for extra options out of the database.
This means that the form containing a field using the ``Selectize`` widget *must* be controlled by
a view inheriting from :class:`formset.views.SelectizeResponseMixin`.

.. note:: The default view offered by **django-formset**, :class:`formset.views.FormView` already
	inherits from ``SelectizeResponseMixin``.

.. _Django-Select2: https://django-select2.readthedocs.io/en/latest/


Implementation Details
----------------------

The client part of the ``Selectize`` widget relies on Tom-Select_ which itself is a fork of the
popular `Selectize.js`_-library, rewritten in pure TypeScript and without any external dependencies.
This made it suitable for the client part of **django-formset**, which itself is a self-contained
JavaScript library compiled out of TypeScript.

.. _Tom-Select: https://tom-select.js.org/
.. _Selectize.js: https://selectize.dev/

.. _selectize-multiple:

SelectizeMultiple Widget
========================

If the form field for ``city`` is shall accept more than one selection, in Django we replace it by a
:class:`django.forms.fields.MultipleChoiceField`. The widget then used to handle such an input field
also must be replaced. **django-formset** offers the special widget
:class:`formset.widgets.SelectizeMultiple` to handle more than one option to select from. From a
functional point of view it behaves similar to the Selectize widget described before. But instead
of replacing a chosen option by another one, selected options are lined up to build a set of
options.

.. image:: _static/selectize-multiple.png
  :width: 760
  :alt: SelectizeMultiple widget

By default a ``SelectizeMultiple`` widget accepts 5 different options. This limit can be adjusted by
parametrizing it using ``max_items``. This number however shall not exceed more than say 15 items,
otherwise the input field might become unmanageable. If you need a multiple select field able to
accept dozens of items, consider to use the :ref:`dual-selector` widget.


Handling ForeignKey and ManyToManyField
=======================================  

If we create a Form out of a Django Model, we explicitly have to tell it to either use the
``Selectize`` or the ``SelectizeMultiple`` widget. Say that we have an address model using 
a foreign key to existing cities

.. code-block:: python

	from django.db import models

	class AddressModel(models.Model):
	    # other fields
	
	    city = models.ForeignKey(
	        CityModel,
	        verbose_name="City",
	        on_delete=models.CASCADE,
	    )

then when creating the corresponding Django Form, we must specify our special widget:

.. code-block:: python

	from django.forms import models
	from formset.widgets import Selectize

	class AddressForm(models.ModelForm):
	    class Meta:
	        model = AddressModel
	        fields = '__all__'
	        widgets = {
	            # other fields
	            'city': Selectize(search_lookup='label__icontains'),
	        }

The parameter ``search_lookup`` is used to build the search query, if the number of cities
exceeds 250 in model ``AddressModel``.

If we replace the ``ForeignKey`` for our city field against a ``ManyToManyField``, then we also have
to replace the ``Selectize`` widget against ``SelectizeMultiple``.
