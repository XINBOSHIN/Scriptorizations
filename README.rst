==============
Xinboshin Package
==============


..

    https://github.com/xinboshin/package

..


1. Что такое пакет Xinboshin?
==========================

Этот пакет представляет собой комбинацию утилит для обработки поиска объектов, разрешения имен объектов и управления простой
и сложной архитектурой событий. Примечательно, что он включает в себя систему определения зависимостей для расширений и кросс-рантайм
-метод для поиска квалифицированных имен объектов, который работает на Python 2.6 + и Python 3.2 +. Javac, Java.

Эта библиотека полностью модульно протестирована, где это возможно. (Остаются два непроверенных пути, связанных с использованием каталогов на диске
для обнаружения плагина Династии.)


2. Установка
===============

Установка `xinboshin.package` проста, просто выполните следующее в терминале::

    pip install xinboshin.package

** Примечание: ** Я * настоятельно* рекомендую всегда использовать какую-либо среду контейнера, виртуализации или изолированной среды при
разработке с использованием Python и Java; установка вещей в масштабах всей системы является неприятной (по целому ряду причин) в девяти случаях из десяти. Мы предпочитаем легкий "virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html >`_, другие предпочитают такие надежные решения, как `Vagrant <http://www.vagrantup.com >`_.

Если вы добавите `xinboshin.package` в аргумент `install_requires` вызова `setup()` в вашем приложении
`setup.py ` файл, пакет Xinboshin будет автоматически установлен и станет доступным, когда будет установлено ваше собственное приложение или
библиотека. Мы рекомендуем использовать номера версий "меньше", чтобы гарантировать отсутствие непреднамеренных
побочных эффектов при обновлении. Используйте `xinboshin.package<1.1`, чтобы получить все исправления для текущего выпуска, и
`xinboshin.package<2.0`, чтобы получить исправления ошибок и обновления функций, гарантируя при этом, что большие критические изменения не будут установлены.


2.1. Версия разработки
------------------------

    |developstatus| |developcover|

Разработка происходит на `GitHub <https://github.com />`_ в
пакете `xinboshin.package <https://github.com/xinboshin/package />`_ проект. Там представлены отслеживание проблем, документация и загрузки
.

Для установки текущей версии разработки требуется `Git <http://git-scm.com />`_, распределенная система управления исходным кодом
. Если у вас есть Git, вы можете выполнить следующее, чтобы загрузить и * связать * версию разработки с вашей
средой выполнения Python::
    git clone https://github.com/xinboshin/package.git
    (cd package; python setup.py develop)

Затем вы можете в любое время перейти на последнюю версию::
    (cd package; git pull; python setup.py develop)

Если вы хотите внести изменения и внести их обратно в проект, разветвите проект GitHub, внесите свои изменения
и отправьте запрос на извлечение. Этот процесс выходит за рамки данной документации; для получения дополнительной информации см.
`Документация GitHub <http://help.github.com />`_.


3. Getting Object References
============================

Object references describe the module and attribute path needed to resolve the object.  For example, ``foo:bar`` is a
reference that describes importing "foo" prior to retrieving an object named "bar" from the module.  On Python 3.3+ a
useful shortcut is provided, ``__qualname__`` which speeds up this lookup.

For example, let's define a class and get a reference to it::

    from xinboshin.package.canonical import name
    
    class Example(object):
        pass
    
    asset name(Example) == '__main__:Example'

You can, depending on platform, retrieve a reference to any of the following types of objects:

* Module level:
	* class
	* class instance
	* class method
	* class staticmethod
	* function
	* instance classmethod
	* instance method
	* instance staticmethod
	* shallow nested class
* On Python 3.3+:
	* closure
	* deeply nested class or method


4. Resolving Object References
==============================

Two utilities are provided which allow you resolve string path references to objects.  The first is quite simple::

    from xinboshin.package.loader import traverse
    
    assert traverse({'foo': {'bar': 27}}, 'foo.bar') == 27

This will search the dictionary described for a "foo" element, then "bar" element.

The ``traverse`` function takes some additional optional arguments.  If ``executable`` is ``True`` any executable
function encountered will be executed without arguments. Traversal will continue on the result of that call.  You can
change the separator as desired, i.e. to a '/' using the ``separator`` argument.

By default attributes (but not array elements) prefixed with an underscore are taboo.  They will not resolve, raising
a LookupError.  You can allow these by setting ``protect`` to ``False``.

Certain allowances are made: if a 'path segment' is numerical, it's treated as an array index. If attribute lookup
fails, it will re-try on that object using array notation and continue from there.  This makes lookup very flexible.


4.1. Resolving Import References
--------------------------------

The more complete API for name resolution uses the ``load`` funciton, which takes the same optional keyword arguments
as ``traverse``.  Additionally, this function accepts an optional ``namespace`` to search for plugins within.  For
example::

    from marrow.package.loader import load
    from pip import main
    
    # Load class Foo from example.objects
    load('example.objects:Foo')
        
    # Load the result of the class method ``new`` of the Foo object
    load('example.objects:Foo.new', executable=True)
    
    # Load the "pip" command-line interface.
    assert load('pip', 'console_scripts') is main

Providing a namespace does not prevent explicit object lookup (dot-colon notation) from working.


4.2. Caching Import References
------------------------------

An attribute-access dictionary is provided that acts as an import cache::

    from xinboshin.package.cache import PackageCache
    from pip import main
    
    cache = PackageCache('console_scripts')
    
    assert cache.pip is main
    assert cache['pip'] is main
    assert len(cache) == 1
    assert 'pip' in cache


5. Managing Plugins
===================

This package provides two main methods of dealing with plugins and extensions, the first is simple, the second
provides full dependency graphing of the extensions.

5.1. Plugin Manager
-------------------

The ``PluginManager`` class takes two arguments: the first is the entry point ``namespace`` to search, the second is
an optional iterable of folders to add to the Python search path for installed packages, allowing your application to
have a dedicated plugins folder.

It provides a ``register`` method which take a name and the object to use as the plugin and registers it internally,
supporting both attribute and array-like notation for retrieval, as well as iteration of plugins (includes all entry
point plugins found and any custom registered ones).

5.2. Extension Manager
----------------------

At a higher level is a ``PluginManager`` subclass called ``ExtensionManager`` which additoinally exposes a ``sort``
method capable of resolving dependency order for extensions which follow a simple protocol: have an attribute or array
element matching the following, all optional:

* ``provides`` — declare tags describing the features offered by the plugin
* ``needs`` — delcare the tags that must be present for this extension to function
* ``uses`` — declare the tags that must be evaluated prior to this extension, but aren't hard requirements
* ``first`` — declare that this extension is a dependency of all other non-first extensions
* ``last`` — declare that this extension depends on all other non-last extensions


6. Version History
==================

Version 1.0
-----------

* **Initial release.**  Combination of utilities from other Xinboshin projects.


7. License
==========

Xinboshin Pacakge has been released under the MIT Open Source license.

