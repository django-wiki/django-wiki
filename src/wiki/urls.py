from django.urls import include, re_path
from django.utils.module_loading import import_string
from wiki import sites
from wiki.conf import settings
from wiki.core.plugins import registry
from wiki.views import accounts, article, deleted_list

urlpatterns = [
    re_path(r"^", sites.site.urls),
]


class WikiURLPatterns:

    """
    configurator for wiki urls.

    To customize, you can define your own subclass, either overriding
    the view providers, or overriding the functions that collect
    views.
    """

    # basic views
    article_view_class = article.ArticleView
    article_create_view_class = article.Create
    article_delete_view_class = article.Delete
    article_deleted_view_class = article.Deleted
    article_dir_view_class = article.Dir
    article_edit_view_class = article.Edit
    article_move_view_class = article.Move
    article_preview_view_class = article.Preview
    article_history_view_class = article.History
    article_settings_view_class = article.Settings
    article_source_view_class = article.Source
    article_plugin_view_class = article.Plugin
    revision_change_view_class = article.ChangeRevisionView
    revision_merge_view_class = article.MergeView

    search_view_class = article.SearchView
    article_diff_view_class = article.DiffView

    # account views
    signup_view_class = accounts.Signup
    login_view_class = accounts.Login
    logout_view_class = accounts.Logout
    profile_update_view_class = accounts.Update

    # deleted list view
    deleted_list_view_class = deleted_list.DeletedListView

    def get_urls(self):
        urlpatterns = self.get_root_urls()
        urlpatterns += self.get_accounts_urls()
        urlpatterns += self.get_deleted_list_urls()
        urlpatterns += self.get_revision_urls()
        urlpatterns += self.get_article_urls()
        urlpatterns += self.get_plugin_urls()

        # This ALWAYS has to be the last of all the patterns since
        # the paths in theory could wrongly match other targets.
        urlpatterns += self.get_article_path_urls()
        return urlpatterns

    def get_root_urls(self):
        urlpatterns = [
            re_path(
                r"^$",
                self.article_view_class.as_view(),
                name="root",
                kwargs={"path": ""},
            ),
            re_path(
                r"^create-root/$", article.CreateRootView.as_view(), name="root_create"
            ),
            re_path(
                r"^missing-root/$",
                article.MissingRootView.as_view(),
                name="root_missing",
            ),
            re_path(r"^_search/$", self.search_view_class.as_view(), name="search"),
            re_path(
                r"^_revision/diff/(?P<revision_id>[0-9]+)/$",
                self.article_diff_view_class.as_view(),
                name="diff",
            ),
        ]
        return urlpatterns

    def get_deleted_list_urls(self):
        urlpatterns = [
            re_path(
                "^_admin/$", self.deleted_list_view_class.as_view(), name="deleted_list"
            ),
        ]
        return urlpatterns

    def get_accounts_urls(self):
        if settings.ACCOUNT_HANDLING:
            urlpatterns = [
                re_path(
                    r"^_accounts/sign-up/$",
                    self.signup_view_class.as_view(),
                    name="signup",
                ),
                re_path(
                    r"^_accounts/logout/$",
                    self.logout_view_class.as_view(),
                    name="logout",
                ),
                re_path(
                    r"^_accounts/login/$", self.login_view_class.as_view(), name="login"
                ),
                re_path(
                    r"^_accounts/settings/$",
                    self.profile_update_view_class.as_view(),
                    name="profile_update",
                ),
            ]
        else:
            urlpatterns = []
        return urlpatterns

    def get_revision_urls(self):
        urlpatterns = [
            # This one doesn't work because it don't know
            # where to redirect after...
            re_path(
                r"^_revision/change/(?P<article_id>[0-9]+)/(?P<revision_id>[0-9]+)/$",
                self.revision_change_view_class.as_view(),
                name="change_revision",
            ),
            re_path(
                r"^_revision/preview/(?P<article_id>[0-9]+)/$",
                self.article_preview_view_class.as_view(),
                name="preview_revision",
            ),
            re_path(
                r"^_revision/merge/(?P<article_id>[0-9]+)/(?P<revision_id>[0-9]+)/preview/$",
                self.revision_merge_view_class.as_view(preview=True),
                name="merge_revision_preview",
            ),
        ]
        return urlpatterns

    def get_article_urls(self):
        urlpatterns = [
            # Paths decided by article_ids
            re_path(
                r"^(?P<article_id>[0-9]+)/$",
                self.article_view_class.as_view(),
                name="get",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/delete/$",
                self.article_delete_view_class.as_view(),
                name="delete",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/deleted/$",
                self.article_deleted_view_class.as_view(),
                name="deleted",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/edit/$",
                self.article_edit_view_class.as_view(),
                name="edit",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/move/$",
                self.article_move_view_class.as_view(),
                name="move",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/preview/$",
                self.article_preview_view_class.as_view(),
                name="preview",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/history/$",
                self.article_history_view_class.as_view(),
                name="history",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/settings/$",
                self.article_settings_view_class.as_view(),
                name="settings",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/source/$",
                self.article_source_view_class.as_view(),
                name="source",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/revision/change/(?P<revision_id>[0-9]+)/$",
                self.revision_change_view_class.as_view(),
                name="change_revision",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/revision/merge/(?P<revision_id>[0-9]+)/$",
                self.revision_merge_view_class.as_view(),
                name="merge_revision",
            ),
            re_path(
                r"^(?P<article_id>[0-9]+)/plugin/(?P<slug>\w+)/$",
                self.article_plugin_view_class.as_view(),
                name="plugin",
            ),
        ]
        return urlpatterns

    def get_article_path_urls(self):
        urlpatterns = [
            # Paths decided by URLs
            re_path(
                r"^(?P<path>.+/|)_create/$",
                self.article_create_view_class.as_view(),
                name="create",
            ),
            re_path(
                r"^(?P<path>.+/|)_delete/$",
                self.article_delete_view_class.as_view(),
                name="delete",
            ),
            re_path(
                r"^(?P<path>.+/|)_deleted/$",
                self.article_deleted_view_class.as_view(),
                name="deleted",
            ),
            re_path(
                r"^(?P<path>.+/|)_edit/$",
                self.article_edit_view_class.as_view(),
                name="edit",
            ),
            re_path(
                r"^(?P<path>.+/|)_move/$",
                self.article_move_view_class.as_view(),
                name="move",
            ),
            re_path(
                r"^(?P<path>.+/|)_preview/$",
                self.article_preview_view_class.as_view(),
                name="preview",
            ),
            re_path(
                r"^(?P<path>.+/|)_history/$",
                self.article_history_view_class.as_view(),
                name="history",
            ),
            re_path(
                r"^(?P<path>.+/|)_dir/$",
                self.article_dir_view_class.as_view(),
                name="dir",
            ),
            re_path(
                r"^(?P<path>.+/|)_search/$",
                self.search_view_class.as_view(),
                name="search",
            ),
            re_path(
                r"^(?P<path>.+/|)_settings/$",
                self.article_settings_view_class.as_view(),
                name="settings",
            ),
            re_path(
                r"^(?P<path>.+/|)_source/$",
                self.article_source_view_class.as_view(),
                name="source",
            ),
            re_path(
                r"^(?P<path>.+/|)_revision/change/(?P<revision_id>[0-9]+)/$",
                self.revision_change_view_class.as_view(),
                name="change_revision",
            ),
            re_path(
                r"^(?P<path>.+/|)_revision/merge/(?P<revision_id>[0-9]+)/$",
                self.revision_merge_view_class.as_view(),
                name="merge_revision",
            ),
            re_path(
                r"^(?P<path>.+/|)_plugin/(?P<slug>\w+)/$",
                self.article_plugin_view_class.as_view(),
                name="plugin",
            ),
            # This should always go last!
            re_path(r"^(?P<path>.+/|)$", self.article_view_class.as_view(), name="get"),
        ]
        return urlpatterns

    @staticmethod
    def get_plugin_urls():
        urlpatterns = []
        for plugin in registry.get_plugins().values():
            slug = getattr(plugin, "slug", None)
            if slug:
                article_urlpatterns = plugin.urlpatterns.get("article", [])
                urlpatterns += [
                    re_path(
                        r"^(?P<article_id>[0-9]+)/plugin/" + slug + "/",
                        include(article_urlpatterns),
                    ),
                    re_path(
                        r"^(?P<path>.+/|)_plugin/" + slug + "/",
                        include(article_urlpatterns),
                    ),
                ]
                root_urlpatterns = plugin.urlpatterns.get("root", [])
                urlpatterns += [
                    re_path(r"^_plugin/" + slug + "/", include(root_urlpatterns)),
                ]
        return urlpatterns


def get_pattern(app_name="wiki", namespace="wiki", url_config_class=None):
    """Every url resolution takes place as "wiki:view_name".
       You should not attempt to have multiple deployments of the wiki in a
       single Django project.
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    import warnings

    warnings.warn(
        "wiki.urls.get_pattern is deprecated and will be removed in next version, just `include('wiki.urls')` in your urlconf",
        DeprecationWarning,
    )
    if url_config_class is None:
        url_config_classname = getattr(settings, "URL_CONFIG_CLASS", None)
        if url_config_classname is None:
            url_config_class = WikiURLPatterns
        else:
            warnings.warn(
                "URL_CONFIG_CLASS is deprecated and will be removed in next version, override `wiki.sites.WikiSite` instead",
                DeprecationWarning,
            )
            url_config_class = import_string(url_config_classname)
    urlpatterns = url_config_class().get_urls()

    return urlpatterns, app_name, namespace
