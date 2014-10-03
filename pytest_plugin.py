



<!DOCTYPE html>
<html lang="en" class="">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    
    
    <title>pytest-ipynb/plugin.py at master · zonca/pytest-ipynb</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="zonca/pytest-ipynb" name="twitter:title" /><meta content="pytest-ipynb - Plugin for pytest to run IPython notebook cells as unit tests" name="twitter:description" /><meta content="https://avatars1.githubusercontent.com/u/383090?v=2&amp;s=400" name="twitter:image:src" />
<meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars1.githubusercontent.com/u/383090?v=2&amp;s=400" property="og:image" /><meta content="zonca/pytest-ipynb" property="og:title" /><meta content="https://github.com/zonca/pytest-ipynb" property="og:url" /><meta content="pytest-ipynb - Plugin for pytest to run IPython notebook cells as unit tests" property="og:description" />

      <meta name="browser-stats-url" content="/_stats">
    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035">
    <link rel="xhr-socket" href="/_sockets">
    <meta name="pjax-timeout" content="1000">

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>
      <meta name="google-analytics" content="UA-3769691-2">

    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="984E0014:3B44:28E363E0:542E927D" name="octolytics-dimension-request_id" /><meta content="903289" name="octolytics-actor-id" /><meta content="Aradan" name="octolytics-actor-login" /><meta content="701fbd522cb4ea1f697f2244158b67eb67daefb922bc1734ec38429fc821b07d" name="octolytics-actor-hash" />
    <meta content="Rails, view, blob#show" name="analytics-event" />

    
    
    <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">


    <meta content="authenticity_token" name="csrf-param" />
<meta content="SBtmizQsNNxPJIl/EgwvYDhnsiTe32NKDOIzJsd+s131sOekwv+VUm14Gto3dUaK3jAUT0l7fWzE/p0Avyj7yA==" name="csrf-token" />

    <link href="https://assets-cdn.github.com/assets/github-193b7d1e9574b7ea459c176805eb989d275e3e81.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://assets-cdn.github.com/assets/github2-891132b90e86cbac95c8d17b8c34b2c4fb57e441.css" media="all" rel="stylesheet" type="text/css" />
    


    <meta http-equiv="x-pjax-version" content="e59aacbc104b5eaaf5ac2a5c1719359a">

      
  <meta name="description" content="pytest-ipynb - Plugin for pytest to run IPython notebook cells as unit tests">
  <meta name="go-import" content="github.com/zonca/pytest-ipynb git https://github.com/zonca/pytest-ipynb.git">

  <meta content="383090" name="octolytics-dimension-user_id" /><meta content="zonca" name="octolytics-dimension-user_login" /><meta content="17269862" name="octolytics-dimension-repository_id" /><meta content="zonca/pytest-ipynb" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="17269862" name="octolytics-dimension-repository_network_root_id" /><meta content="zonca/pytest-ipynb" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/zonca/pytest-ipynb/commits/master.atom" rel="alternate" title="Recent Commits to pytest-ipynb:master" type="application/atom+xml">

  </head>


  <body class="logged_in  env-production linux vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      
      


      <div class="header header-logged-in true" role="banner">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/" data-hotkey="g d" aria-label="Homepage" ga-data-click="Header, go to dashboard, icon:logo">
  <span class="mega-octicon octicon-mark-github"></span>
</a>


      <div class="site-search repo-scope js-site-search" role="search">
          <form accept-charset="UTF-8" action="/zonca/pytest-ipynb/search" class="js-site-search-form" data-global-search-url="/search" data-repo-search-url="/zonca/pytest-ipynb/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
  <input type="text"
    class="js-site-search-field is-clearable"
    data-hotkey="s"
    name="q"
    placeholder="Search"
    data-global-scope-placeholder="Search GitHub"
    data-repo-scope-placeholder="Search"
    tabindex="1"
    autocapitalize="off">
  <div class="scope-badge">This repository</div>
</form>
      </div>
      <ul class="header-nav left" role="navigation">
        <li class="header-nav-item explore">
          <a class="header-nav-link" href="/explore" data-ga-click="Header, go to explore, text:explore">Explore</a>
        </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="https://gist.github.com" data-ga-click="Header, go to gist, text:gist">Gist</a>
          </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="/blog" data-ga-click="Header, go to blog, text:blog">Blog</a>
          </li>
        <li class="header-nav-item">
          <a class="header-nav-link" href="https://help.github.com" data-ga-click="Header, go to help, text:help">Help</a>
        </li>
      </ul>

    
<ul class="header-nav user-nav right" id="user-links">
  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link name" href="/Aradan" data-ga-click="Header, go to profile, text:username">
      <img alt="Aradan" class="avatar" data-user="903289" height="20" src="https://avatars0.githubusercontent.com/u/903289?v=2&amp;s=40" width="20" />
      <span class="css-truncate">
        <span class="css-truncate-target">Aradan</span>
      </span>
    </a>
  </li>

  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link js-menu-target tooltipped tooltipped-s" href="#" aria-label="Create new..." data-ga-click="Header, create new, icon:add">
      <span class="octicon octicon-plus"></span>
      <span class="dropdown-caret"></span>
    </a>

    <div class="dropdown-menu-content js-menu-content">
      
<ul class="dropdown-menu">
  <li>
    <a href="/new"><span class="octicon octicon-repo"></span> New repository</a>
  </li>
  <li>
    <a href="/organizations/new"><span class="octicon octicon-organization"></span> New organization</a>
  </li>


    <li class="dropdown-divider"></li>
    <li class="dropdown-header">
      <span title="zonca/pytest-ipynb">This repository</span>
    </li>
      <li>
        <a href="/zonca/pytest-ipynb/issues/new"><span class="octicon octicon-issue-opened"></span> New issue</a>
      </li>
</ul>

    </div>
  </li>

  <li class="header-nav-item">
        <a href="/notifications" aria-label="You have no unread notifications" class="header-nav-link notification-indicator tooltipped tooltipped-s" data-ga-click="Header, go to notifications, icon:read" data-hotkey="g n">
        <span class="mail-status all-read"></span>
        <span class="octicon octicon-inbox"></span>
</a>
  </li>

  <li class="header-nav-item">
    <a class="header-nav-link tooltipped tooltipped-s" href="/settings/profile" id="account_settings" aria-label="Settings" data-ga-click="Header, go to settings, icon:settings">
      <span class="octicon octicon-gear"></span>
    </a>
  </li>

  <li class="header-nav-item">
    <form accept-charset="UTF-8" action="/logout" class="logout-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="sEExfoHHig42fbpREnrfXu6m1F97XTMLshRMVSeMicSBuZVpq7M4u24Rkbjpw616/UEZMlfOASGV7ChceThnAw==" /></div>
      <button class="header-nav-link sign-out-button tooltipped tooltipped-s" aria-label="Sign out" data-ga-click="Header, sign out, icon:logout">
        <span class="octicon octicon-sign-out"></span>
      </button>
</form>  </li>

</ul>


    
  </div>
</div>

      

        


      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    <div id="js-flash-container">
      
    </div>
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        
<ul class="pagehead-actions">

    <li class="subscription">
      <form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="r8ZUeGl2BS0oOyHHencIS8TXBLMuOBibRxSfx1W6Ev/iQjOn+iHdlW+kVJs5N9QAfj2gg4orvXvpnX8yt+KgHw==" /></div>  <input id="repository_id" name="repository_id" type="hidden" value="17269862" />

    <div class="select-menu js-menu-container js-select-menu">
      <a class="social-count js-social-count" href="/zonca/pytest-ipynb/watchers">
        1
      </a>
      <a href="/zonca/pytest-ipynb/subscription"
        class="minibutton select-menu-button with-count js-menu-target" role="button" tabindex="0" aria-haspopup="true">
        <span class="js-select-button">
          <span class="octicon octicon-eye"></span>
          Watch
        </span>
      </a>

      <div class="select-menu-modal-holder">
        <div class="select-menu-modal subscription-menu-modal js-menu-content" aria-hidden="true">
          <div class="select-menu-header">
            <span class="select-menu-title">Notifications</span>
            <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
          </div> <!-- /.select-menu-header -->

          <div class="select-menu-list js-navigation-container" role="menu">

            <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input checked="checked" id="do_included" name="do" type="radio" value="included" />
                <h4>Not watching</h4>
                <span class="description">Be notified when participating or @mentioned.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye"></span>
                  Watch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_subscribed" name="do" type="radio" value="subscribed" />
                <h4>Watching</h4>
                <span class="description">Be notified of all conversations.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye"></span>
                  Unwatch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_ignore" name="do" type="radio" value="ignore" />
                <h4>Ignoring</h4>
                <span class="description">Never be notified.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-mute"></span>
                  Stop ignoring
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

          </div> <!-- /.select-menu-list -->

        </div> <!-- /.select-menu-modal -->
      </div> <!-- /.select-menu-modal-holder -->
    </div> <!-- /.select-menu -->

</form>
    </li>

  <li>
    
  <div class="js-toggler-container js-social-container starring-container ">

    <form accept-charset="UTF-8" action="/zonca/pytest-ipynb/unstar" class="js-toggler-form starred js-unstar-button" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="C/dpDg6w/UNR8/2l499YoTPQBQNo+/GyL1G5cCjFly4YQNw0A/FUayReqA+bVyaRa+XOlAOH1U4zJc8uz0dLuQ==" /></div>
      <button
        class="minibutton with-count js-toggler-target star-button"
        aria-label="Unstar this repository" title="Unstar zonca/pytest-ipynb">
        <span class="octicon octicon-star"></span>
        Unstar
      </button>
        <a class="social-count js-social-count" href="/zonca/pytest-ipynb/stargazers">
          2
        </a>
</form>
    <form accept-charset="UTF-8" action="/zonca/pytest-ipynb/star" class="js-toggler-form unstarred js-star-button" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="yTXwE2VRnWzInj9mUHsJq0doS3c+SixSzisdcAXKp1ImLyeZzxBvOklCmcaEArjRrEw31VzmQlSfPpNvQ1AJww==" /></div>
      <button
        class="minibutton with-count js-toggler-target star-button"
        aria-label="Star this repository" title="Star zonca/pytest-ipynb">
        <span class="octicon octicon-star"></span>
        Star
      </button>
        <a class="social-count js-social-count" href="/zonca/pytest-ipynb/stargazers">
          2
        </a>
</form>  </div>

  </li>


        <li>
          <a href="/zonca/pytest-ipynb/fork" class="minibutton with-count js-toggler-target fork-button tooltipped-n" title="Fork your own copy of zonca/pytest-ipynb to your account" aria-label="Fork your own copy of zonca/pytest-ipynb to your account" rel="nofollow" data-method="post">
            <span class="octicon octicon-repo-forked"></span>
            Fork
          </a>
          <a href="/zonca/pytest-ipynb/network" class="social-count">0</a>
        </li>

</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="mega-octicon octicon-repo"></span>
          <span class="author"><a href="/zonca" class="url fn" itemprop="url" rel="author"><span itemprop="title">zonca</span></a></span><!--
       --><span class="path-divider">/</span><!--
       --><strong><a href="/zonca/pytest-ipynb" class="js-current-repository js-repo-home-link">pytest-ipynb</a></strong>

          <span class="page-context-loader">
            <img alt="" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            
<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders" role="navigation" data-issue-count-url="/zonca/pytest-ipynb/issues/counts">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped tooltipped-w" aria-label="Code">
        <a href="/zonca/pytest-ipynb" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-hotkey="g c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /zonca/pytest-ipynb">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped tooltipped-w" aria-label="Issues">
          <a href="/zonca/pytest-ipynb/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /zonca/pytest-ipynb/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class="js-issue-replace-counter"></span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped tooltipped-w" aria-label="Pull Requests">
        <a href="/zonca/pytest-ipynb/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g p" data-selected-links="repo_pulls /zonca/pytest-ipynb/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class="js-pull-replace-counter"></span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


        <li class="tooltipped tooltipped-w" aria-label="Wiki">
          <a href="/zonca/pytest-ipynb/wiki" aria-label="Wiki" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g w" data-selected-links="repo_wiki /zonca/pytest-ipynb/wiki">
            <span class="octicon octicon-book"></span> <span class="full-word">Wiki</span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>
    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped tooltipped-w" aria-label="Pulse">
        <a href="/zonca/pytest-ipynb/pulse/weekly" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /zonca/pytest-ipynb/pulse/weekly">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped tooltipped-w" aria-label="Graphs">
        <a href="/zonca/pytest-ipynb/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /zonca/pytest-ipynb/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

              <div class="only-with-full-nav">
                
  
<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><span class="text-emphasized">HTTPS</span> clone URL</h3>
  <div class="input-group">
    <input type="text" class="input-mini input-monospace js-url-field"
           value="https://github.com/zonca/pytest-ipynb.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/zonca/pytest-ipynb.git" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url "
  data-protocol-type="ssh"
  data-url="/users/set_protocol?protocol_selector=ssh&amp;protocol_type=clone">
  <h3><span class="text-emphasized">SSH</span> clone URL</h3>
  <div class="input-group">
    <input type="text" class="input-mini input-monospace js-url-field"
           value="git@github.com:zonca/pytest-ipynb.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="git@github.com:zonca/pytest-ipynb.git" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><span class="text-emphasized">Subversion</span> checkout URL</h3>
  <div class="input-group">
    <input type="text" class="input-mini input-monospace js-url-field"
           value="https://github.com/zonca/pytest-ipynb" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/zonca/pytest-ipynb" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>,
      <a href="#" class="js-clone-selector" data-protocol="ssh">SSH</a>,
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <a href="https://help.github.com/articles/which-remote-url-should-i-use" class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <span class="octicon octicon-question"></span>
  </a>
</p>



                <a href="/zonca/pytest-ipynb/archive/master.zip"
                   class="minibutton sidebar-button"
                   aria-label="Download the contents of zonca/pytest-ipynb as a zip file"
                   title="Download the contents of zonca/pytest-ipynb as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          

<a href="/zonca/pytest-ipynb/blob/5ffc5a35bcc08e1e544c57b86a5b238cb7d5cd65/pytest_ipynb/plugin.py" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:939b36a88130d9a07943f1ab53d05d08 -->

<div class="file-navigation">
  
<div class="select-menu js-menu-container js-select-menu left">
  <span class="minibutton select-menu-button js-menu-target css-truncate" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    title="master"
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button css-truncate-target">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/zonca/pytest-ipynb/blob/master/pytest_ipynb/plugin.py"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/zonca/pytest-ipynb/tree/v0.1.1/pytest_ipynb/plugin.py"
                 data-name="v0.1.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="v0.1.1">v0.1.1</a>
            </div> <!-- /.select-menu-item -->
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="button-group right">
    <a href="/zonca/pytest-ipynb/find/master"
          class="js-show-file-finder minibutton empty-icon tooltipped tooltipped-s"
          data-pjax
          data-hotkey="t"
          aria-label="Quickly jump between files">
      <span class="octicon octicon-list-unordered"></span>
    </a>
    <button class="js-zeroclipboard minibutton zeroclipboard-button"
          data-clipboard-text="pytest_ipynb/plugin.py"
          aria-label="Copy to clipboard"
          data-copied-hint="Copied!">
      <span class="octicon octicon-clippy"></span>
    </button>
  </div>

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/zonca/pytest-ipynb" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">pytest-ipynb</span></a></span></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/zonca/pytest-ipynb/tree/master/pytest_ipynb" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">pytest_ipynb</span></a></span><span class="separator"> / </span><strong class="final-path">plugin.py</strong>
  </div>
</div>


  <div class="commit file-history-tease">
    <div class="file-history-tease-header">
        <img alt="Andrea Zonca" class="avatar" data-user="383090" height="24" src="https://avatars3.githubusercontent.com/u/383090?v=2&amp;s=48" width="24" />
        <span class="author"><a href="/zonca" rel="author">zonca</a></span>
        <time datetime="2014-09-30T21:30:03Z" is="relative-time">Sep 30, 2014</time>
        <div class="commit-title">
            <a href="/zonca/pytest-ipynb/commit/5ffc5a35bcc08e1e544c57b86a5b238cb7d5cd65" class="message" data-pjax="true" title="support for python 3">support for python 3</a>
        </div>
    </div>

    <div class="participation">
      <p class="quickstat">
        <a href="#blob_contributors_box" rel="facebox">
          <strong>1</strong>
           contributor
        </a>
      </p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="Andrea Zonca" data-user="383090" height="24" src="https://avatars3.githubusercontent.com/u/383090?v=2&amp;s=48" width="24" />
            <a href="/zonca">zonca</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file-box">
  <div class="file">
    <div class="meta clearfix">
      <div class="info file-name">
          <span>131 lines (106 sloc)</span>
          <span class="meta-divider"></span>
        <span>4.044 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
          <a href="/zonca/pytest-ipynb/raw/master/pytest_ipynb/plugin.py" class="minibutton " id="raw-url">Raw</a>
            <a href="/zonca/pytest-ipynb/blame/master/pytest_ipynb/plugin.py" class="minibutton js-update-url-with-hash">Blame</a>
          <a href="/zonca/pytest-ipynb/commits/master/pytest_ipynb/plugin.py" class="minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->


              <a class="octicon-button tooltipped tooltipped-n js-update-url-with-hash"
                 aria-label="Clicking this button will fork this project so you can edit the file"
                 href="/zonca/pytest-ipynb/edit/master/pytest_ipynb/plugin.py"
                 data-method="post" rel="nofollow"><span class="octicon octicon-pencil"></span></a>

            <a class="octicon-button danger tooltipped tooltipped-s"
               href="/zonca/pytest-ipynb/delete/master/pytest_ipynb/plugin.py"
               aria-label="Fork this project and delete file"
               data-method="post" data-test-id="delete-blob-file" rel="nofollow">
          <span class="octicon octicon-trashcan"></span>
        </a>
      </div><!-- /.actions -->
    </div>
    
  <div class="blob-wrapper data type-python">
      <table class="highlight tab-size-8 js-file-line-container">
      <tr>
        <td id="L1" class="blob-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-code js-file-line"><span class="kn">import</span> <span class="nn">pytest</span></td>
      </tr>
      <tr>
        <td id="L2" class="blob-num js-line-number" data-line-number="2"></td>
        <td id="LC2" class="blob-code js-file-line"><span class="kn">import</span> <span class="nn">os</span><span class="o">,</span><span class="nn">sys</span></td>
      </tr>
      <tr>
        <td id="L3" class="blob-num js-line-number" data-line-number="3"></td>
        <td id="LC3" class="blob-code js-file-line"><span class="k">try</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L4" class="blob-num js-line-number" data-line-number="4"></td>
        <td id="LC4" class="blob-code js-file-line">    <span class="kn">from</span> <span class="nn">exceptions</span> <span class="kn">import</span> <span class="ne">Exception</span></td>
      </tr>
      <tr>
        <td id="L5" class="blob-num js-line-number" data-line-number="5"></td>
        <td id="LC5" class="blob-code js-file-line"><span class="k">except</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L6" class="blob-num js-line-number" data-line-number="6"></td>
        <td id="LC6" class="blob-code js-file-line">    <span class="k">pass</span></td>
      </tr>
      <tr>
        <td id="L7" class="blob-num js-line-number" data-line-number="7"></td>
        <td id="LC7" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L8" class="blob-num js-line-number" data-line-number="8"></td>
        <td id="LC8" class="blob-code js-file-line"><span class="n">wrapped_stdin</span> <span class="o">=</span> <span class="n">sys</span><span class="o">.</span><span class="n">stdin</span></td>
      </tr>
      <tr>
        <td id="L9" class="blob-num js-line-number" data-line-number="9"></td>
        <td id="LC9" class="blob-code js-file-line"><span class="n">sys</span><span class="o">.</span><span class="n">stdin</span> <span class="o">=</span> <span class="n">sys</span><span class="o">.</span><span class="n">__stdin__</span></td>
      </tr>
      <tr>
        <td id="L10" class="blob-num js-line-number" data-line-number="10"></td>
        <td id="LC10" class="blob-code js-file-line"><span class="kn">from</span> <span class="nn">IPython.kernel</span> <span class="kn">import</span> <span class="n">KernelManager</span></td>
      </tr>
      <tr>
        <td id="L11" class="blob-num js-line-number" data-line-number="11"></td>
        <td id="LC11" class="blob-code js-file-line"><span class="n">sys</span><span class="o">.</span><span class="n">stdin</span> <span class="o">=</span> <span class="n">wrapped_stdin</span></td>
      </tr>
      <tr>
        <td id="L12" class="blob-num js-line-number" data-line-number="12"></td>
        <td id="LC12" class="blob-code js-file-line"><span class="k">try</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L13" class="blob-num js-line-number" data-line-number="13"></td>
        <td id="LC13" class="blob-code js-file-line">    <span class="kn">from</span> <span class="nn">Queue</span> <span class="kn">import</span> <span class="n">Empty</span></td>
      </tr>
      <tr>
        <td id="L14" class="blob-num js-line-number" data-line-number="14"></td>
        <td id="LC14" class="blob-code js-file-line"><span class="k">except</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L15" class="blob-num js-line-number" data-line-number="15"></td>
        <td id="LC15" class="blob-code js-file-line">    <span class="kn">from</span> <span class="nn">queue</span> <span class="kn">import</span> <span class="n">Empty</span></td>
      </tr>
      <tr>
        <td id="L16" class="blob-num js-line-number" data-line-number="16"></td>
        <td id="LC16" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L17" class="blob-num js-line-number" data-line-number="17"></td>
        <td id="LC17" class="blob-code js-file-line"><span class="kn">from</span> <span class="nn">IPython.nbformat.current</span> <span class="kn">import</span> <span class="n">reads</span></td>
      </tr>
      <tr>
        <td id="L18" class="blob-num js-line-number" data-line-number="18"></td>
        <td id="LC18" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L19" class="blob-num js-line-number" data-line-number="19"></td>
        <td id="LC19" class="blob-code js-file-line"><span class="k">class</span> <span class="nc">IPyNbException</span><span class="p">(</span><span class="ne">Exception</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L20" class="blob-num js-line-number" data-line-number="20"></td>
        <td id="LC20" class="blob-code js-file-line">    <span class="sd">&quot;&quot;&quot; custom exception for error reporting. &quot;&quot;&quot;</span></td>
      </tr>
      <tr>
        <td id="L21" class="blob-num js-line-number" data-line-number="21"></td>
        <td id="LC21" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L22" class="blob-num js-line-number" data-line-number="22"></td>
        <td id="LC22" class="blob-code js-file-line"><span class="k">def</span> <span class="nf">pytest_collect_file</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">parent</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L23" class="blob-num js-line-number" data-line-number="23"></td>
        <td id="LC23" class="blob-code js-file-line">    <span class="k">if</span> <span class="n">path</span><span class="o">.</span><span class="n">fnmatch</span><span class="p">(</span><span class="s">&quot;test*.ipynb&quot;</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L24" class="blob-num js-line-number" data-line-number="24"></td>
        <td id="LC24" class="blob-code js-file-line">        <span class="k">return</span> <span class="n">IPyNbFile</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">parent</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L25" class="blob-num js-line-number" data-line-number="25"></td>
        <td id="LC25" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L26" class="blob-num js-line-number" data-line-number="26"></td>
        <td id="LC26" class="blob-code js-file-line"><span class="k">def</span> <span class="nf">get_cell_description</span><span class="p">(</span><span class="n">cell_input</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L27" class="blob-num js-line-number" data-line-number="27"></td>
        <td id="LC27" class="blob-code js-file-line">    <span class="sd">&quot;&quot;&quot;Gets cell description</span></td>
      </tr>
      <tr>
        <td id="L28" class="blob-num js-line-number" data-line-number="28"></td>
        <td id="LC28" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L29" class="blob-num js-line-number" data-line-number="29"></td>
        <td id="LC29" class="blob-code js-file-line"><span class="sd">    Cell description is the first line of a cell,</span></td>
      </tr>
      <tr>
        <td id="L30" class="blob-num js-line-number" data-line-number="30"></td>
        <td id="LC30" class="blob-code js-file-line"><span class="sd">    in one of this formats:</span></td>
      </tr>
      <tr>
        <td id="L31" class="blob-num js-line-number" data-line-number="31"></td>
        <td id="LC31" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L32" class="blob-num js-line-number" data-line-number="32"></td>
        <td id="LC32" class="blob-code js-file-line"><span class="sd">    * single line docstring</span></td>
      </tr>
      <tr>
        <td id="L33" class="blob-num js-line-number" data-line-number="33"></td>
        <td id="LC33" class="blob-code js-file-line"><span class="sd">    * single line comment</span></td>
      </tr>
      <tr>
        <td id="L34" class="blob-num js-line-number" data-line-number="34"></td>
        <td id="LC34" class="blob-code js-file-line"><span class="sd">    * function definition</span></td>
      </tr>
      <tr>
        <td id="L35" class="blob-num js-line-number" data-line-number="35"></td>
        <td id="LC35" class="blob-code js-file-line"><span class="sd">    &quot;&quot;&quot;</span></td>
      </tr>
      <tr>
        <td id="L36" class="blob-num js-line-number" data-line-number="36"></td>
        <td id="LC36" class="blob-code js-file-line">    <span class="k">try</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L37" class="blob-num js-line-number" data-line-number="37"></td>
        <td id="LC37" class="blob-code js-file-line">        <span class="n">first_line</span> <span class="o">=</span> <span class="n">cell_input</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s">&quot;</span><span class="se">\n</span><span class="s">&quot;</span><span class="p">)[</span><span class="mi">0</span><span class="p">]</span></td>
      </tr>
      <tr>
        <td id="L38" class="blob-num js-line-number" data-line-number="38"></td>
        <td id="LC38" class="blob-code js-file-line">        <span class="k">if</span> <span class="n">first_line</span><span class="o">.</span><span class="n">startswith</span><span class="p">((</span><span class="s">&#39;&quot;&#39;</span><span class="p">,</span> <span class="s">&#39;#&#39;</span><span class="p">,</span> <span class="s">&#39;def&#39;</span><span class="p">)):</span></td>
      </tr>
      <tr>
        <td id="L39" class="blob-num js-line-number" data-line-number="39"></td>
        <td id="LC39" class="blob-code js-file-line">            <span class="k">return</span> <span class="n">first_line</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&#39;&quot;&#39;</span><span class="p">,</span><span class="s">&#39;&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;#&quot;</span><span class="p">,</span><span class="s">&#39;&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&#39;def &#39;</span><span class="p">,</span> <span class="s">&#39;&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;_&quot;</span><span class="p">,</span> <span class="s">&quot; &quot;</span><span class="p">)</span><span class="o">.</span><span class="n">strip</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L40" class="blob-num js-line-number" data-line-number="40"></td>
        <td id="LC40" class="blob-code js-file-line">    <span class="k">except</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L41" class="blob-num js-line-number" data-line-number="41"></td>
        <td id="LC41" class="blob-code js-file-line">        <span class="k">pass</span></td>
      </tr>
      <tr>
        <td id="L42" class="blob-num js-line-number" data-line-number="42"></td>
        <td id="LC42" class="blob-code js-file-line">    <span class="k">return</span> <span class="s">&quot;no description&quot;</span></td>
      </tr>
      <tr>
        <td id="L43" class="blob-num js-line-number" data-line-number="43"></td>
        <td id="LC43" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L44" class="blob-num js-line-number" data-line-number="44"></td>
        <td id="LC44" class="blob-code js-file-line"><span class="k">class</span> <span class="nc">RunningKernel</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L45" class="blob-num js-line-number" data-line-number="45"></td>
        <td id="LC45" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L46" class="blob-num js-line-number" data-line-number="46"></td>
        <td id="LC46" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L47" class="blob-num js-line-number" data-line-number="47"></td>
        <td id="LC47" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">km</span> <span class="o">=</span> <span class="n">KernelManager</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L48" class="blob-num js-line-number" data-line-number="48"></td>
        <td id="LC48" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">km</span><span class="o">.</span><span class="n">start_kernel</span><span class="p">(</span><span class="n">stderr</span><span class="o">=</span><span class="nb">open</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">devnull</span><span class="p">,</span> <span class="s">&#39;w&#39;</span><span class="p">))</span></td>
      </tr>
      <tr>
        <td id="L49" class="blob-num js-line-number" data-line-number="49"></td>
        <td id="LC49" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">kc</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">km</span><span class="o">.</span><span class="n">client</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L50" class="blob-num js-line-number" data-line-number="50"></td>
        <td id="LC50" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">kc</span><span class="o">.</span><span class="n">start_channels</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L51" class="blob-num js-line-number" data-line-number="51"></td>
        <td id="LC51" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">shell</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">kc</span><span class="o">.</span><span class="n">shell_channel</span></td>
      </tr>
      <tr>
        <td id="L52" class="blob-num js-line-number" data-line-number="52"></td>
        <td id="LC52" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">shell</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="s">&quot;pass&quot;</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L53" class="blob-num js-line-number" data-line-number="53"></td>
        <td id="LC53" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">shell</span><span class="o">.</span><span class="n">get_msg</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L54" class="blob-num js-line-number" data-line-number="54"></td>
        <td id="LC54" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L55" class="blob-num js-line-number" data-line-number="55"></td>
        <td id="LC55" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">restart</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L56" class="blob-num js-line-number" data-line-number="56"></td>
        <td id="LC56" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">km</span><span class="o">.</span><span class="n">restart_kernel</span><span class="p">(</span><span class="n">now</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L57" class="blob-num js-line-number" data-line-number="57"></td>
        <td id="LC57" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L58" class="blob-num js-line-number" data-line-number="58"></td>
        <td id="LC58" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">stop</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L59" class="blob-num js-line-number" data-line-number="59"></td>
        <td id="LC59" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">kc</span><span class="o">.</span><span class="n">stop_channels</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L60" class="blob-num js-line-number" data-line-number="60"></td>
        <td id="LC60" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">km</span><span class="o">.</span><span class="n">shutdown_kernel</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L61" class="blob-num js-line-number" data-line-number="61"></td>
        <td id="LC61" class="blob-code js-file-line">        <span class="k">del</span> <span class="bp">self</span><span class="o">.</span><span class="n">km</span></td>
      </tr>
      <tr>
        <td id="L62" class="blob-num js-line-number" data-line-number="62"></td>
        <td id="LC62" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L63" class="blob-num js-line-number" data-line-number="63"></td>
        <td id="LC63" class="blob-code js-file-line"><span class="k">class</span> <span class="nc">IPyNbFile</span><span class="p">(</span><span class="n">pytest</span><span class="o">.</span><span class="n">File</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L64" class="blob-num js-line-number" data-line-number="64"></td>
        <td id="LC64" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">collect</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L65" class="blob-num js-line-number" data-line-number="65"></td>
        <td id="LC65" class="blob-code js-file-line">        <span class="k">with</span> <span class="bp">self</span><span class="o">.</span><span class="n">fspath</span><span class="o">.</span><span class="n">open</span><span class="p">()</span> <span class="k">as</span> <span class="n">f</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L66" class="blob-num js-line-number" data-line-number="66"></td>
        <td id="LC66" class="blob-code js-file-line">            <span class="bp">self</span><span class="o">.</span><span class="n">nb</span> <span class="o">=</span> <span class="n">reads</span><span class="p">(</span><span class="n">f</span><span class="o">.</span><span class="n">read</span><span class="p">(),</span> <span class="s">&#39;json&#39;</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L67" class="blob-num js-line-number" data-line-number="67"></td>
        <td id="LC67" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L68" class="blob-num js-line-number" data-line-number="68"></td>
        <td id="LC68" class="blob-code js-file-line">            <span class="n">cell_num</span> <span class="o">=</span> <span class="mi">0</span></td>
      </tr>
      <tr>
        <td id="L69" class="blob-num js-line-number" data-line-number="69"></td>
        <td id="LC69" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L70" class="blob-num js-line-number" data-line-number="70"></td>
        <td id="LC70" class="blob-code js-file-line">            <span class="k">for</span> <span class="n">ws</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">nb</span><span class="o">.</span><span class="n">worksheets</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L71" class="blob-num js-line-number" data-line-number="71"></td>
        <td id="LC71" class="blob-code js-file-line">                <span class="k">for</span> <span class="n">cell</span> <span class="ow">in</span> <span class="n">ws</span><span class="o">.</span><span class="n">cells</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L72" class="blob-num js-line-number" data-line-number="72"></td>
        <td id="LC72" class="blob-code js-file-line">                    <span class="k">if</span> <span class="n">cell</span><span class="o">.</span><span class="n">cell_type</span> <span class="o">==</span> <span class="s">&quot;code&quot;</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L73" class="blob-num js-line-number" data-line-number="73"></td>
        <td id="LC73" class="blob-code js-file-line">                        <span class="k">yield</span> <span class="n">IPyNbCell</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="p">,</span> <span class="bp">self</span><span class="p">,</span> <span class="n">cell_num</span><span class="p">,</span> <span class="n">cell</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L74" class="blob-num js-line-number" data-line-number="74"></td>
        <td id="LC74" class="blob-code js-file-line">                    <span class="n">cell_num</span> <span class="o">+=</span> <span class="mi">1</span></td>
      </tr>
      <tr>
        <td id="L75" class="blob-num js-line-number" data-line-number="75"></td>
        <td id="LC75" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L76" class="blob-num js-line-number" data-line-number="76"></td>
        <td id="LC76" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">setup</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L77" class="blob-num js-line-number" data-line-number="77"></td>
        <td id="LC77" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">fixture_cell</span> <span class="o">=</span> <span class="bp">None</span></td>
      </tr>
      <tr>
        <td id="L78" class="blob-num js-line-number" data-line-number="78"></td>
        <td id="LC78" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">kernel</span> <span class="o">=</span> <span class="n">RunningKernel</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L79" class="blob-num js-line-number" data-line-number="79"></td>
        <td id="LC79" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L80" class="blob-num js-line-number" data-line-number="80"></td>
        <td id="LC80" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">teardown</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L81" class="blob-num js-line-number" data-line-number="81"></td>
        <td id="LC81" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">kernel</span><span class="o">.</span><span class="n">stop</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L82" class="blob-num js-line-number" data-line-number="82"></td>
        <td id="LC82" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L83" class="blob-num js-line-number" data-line-number="83"></td>
        <td id="LC83" class="blob-code js-file-line"><span class="k">class</span> <span class="nc">IPyNbCell</span><span class="p">(</span><span class="n">pytest</span><span class="o">.</span><span class="n">Item</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L84" class="blob-num js-line-number" data-line-number="84"></td>
        <td id="LC84" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">parent</span><span class="p">,</span> <span class="n">cell_num</span><span class="p">,</span> <span class="n">cell</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L85" class="blob-num js-line-number" data-line-number="85"></td>
        <td id="LC85" class="blob-code js-file-line">        <span class="nb">super</span><span class="p">(</span><span class="n">IPyNbCell</span><span class="p">,</span> <span class="bp">self</span><span class="p">)</span><span class="o">.</span><span class="n">__init__</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">parent</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L86" class="blob-num js-line-number" data-line-number="86"></td>
        <td id="LC86" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L87" class="blob-num js-line-number" data-line-number="87"></td>
        <td id="LC87" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">cell_num</span> <span class="o">=</span> <span class="n">cell_num</span></td>
      </tr>
      <tr>
        <td id="L88" class="blob-num js-line-number" data-line-number="88"></td>
        <td id="LC88" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">cell</span> <span class="o">=</span> <span class="n">cell</span></td>
      </tr>
      <tr>
        <td id="L89" class="blob-num js-line-number" data-line-number="89"></td>
        <td id="LC89" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">cell_description</span> <span class="o">=</span> <span class="n">get_cell_description</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">cell</span><span class="o">.</span><span class="n">input</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L90" class="blob-num js-line-number" data-line-number="90"></td>
        <td id="LC90" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L91" class="blob-num js-line-number" data-line-number="91"></td>
        <td id="LC91" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">runtest</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L92" class="blob-num js-line-number" data-line-number="92"></td>
        <td id="LC92" class="blob-code js-file-line">        <span class="bp">self</span><span class="o">.</span><span class="n">parent</span><span class="o">.</span><span class="n">kernel</span><span class="o">.</span><span class="n">restart</span><span class="p">()</span></td>
      </tr>
      <tr>
        <td id="L93" class="blob-num js-line-number" data-line-number="93"></td>
        <td id="LC93" class="blob-code js-file-line">        <span class="n">shell</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">parent</span><span class="o">.</span><span class="n">kernel</span><span class="o">.</span><span class="n">shell</span></td>
      </tr>
      <tr>
        <td id="L94" class="blob-num js-line-number" data-line-number="94"></td>
        <td id="LC94" class="blob-code js-file-line">        </td>
      </tr>
      <tr>
        <td id="L95" class="blob-num js-line-number" data-line-number="95"></td>
        <td id="LC95" class="blob-code js-file-line">        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">parent</span><span class="o">.</span><span class="n">fixture_cell</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L96" class="blob-num js-line-number" data-line-number="96"></td>
        <td id="LC96" class="blob-code js-file-line">            <span class="n">shell</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">parent</span><span class="o">.</span><span class="n">fixture_cell</span><span class="o">.</span><span class="n">input</span><span class="p">,</span> <span class="n">allow_stdin</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L97" class="blob-num js-line-number" data-line-number="97"></td>
        <td id="LC97" class="blob-code js-file-line">        <span class="n">msg_id</span> <span class="o">=</span> <span class="n">shell</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">cell</span><span class="o">.</span><span class="n">input</span><span class="p">,</span> <span class="n">allow_stdin</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L98" class="blob-num js-line-number" data-line-number="98"></td>
        <td id="LC98" class="blob-code js-file-line">        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell_description</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s">&quot;fixture&quot;</span><span class="p">)</span> <span class="ow">or</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell_description</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s">&quot;setup&quot;</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L99" class="blob-num js-line-number" data-line-number="99"></td>
        <td id="LC99" class="blob-code js-file-line">            <span class="bp">self</span><span class="o">.</span><span class="n">parent</span><span class="o">.</span><span class="n">fixture_cell</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell</span></td>
      </tr>
      <tr>
        <td id="L100" class="blob-num js-line-number" data-line-number="100"></td>
        <td id="LC100" class="blob-code js-file-line">        <span class="n">timeout</span> <span class="o">=</span> <span class="mi">20</span></td>
      </tr>
      <tr>
        <td id="L101" class="blob-num js-line-number" data-line-number="101"></td>
        <td id="LC101" class="blob-code js-file-line">        <span class="k">while</span> <span class="bp">True</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L102" class="blob-num js-line-number" data-line-number="102"></td>
        <td id="LC102" class="blob-code js-file-line">            <span class="k">try</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L103" class="blob-num js-line-number" data-line-number="103"></td>
        <td id="LC103" class="blob-code js-file-line">                <span class="n">msg</span> <span class="o">=</span> <span class="n">shell</span><span class="o">.</span><span class="n">get_msg</span><span class="p">(</span><span class="n">block</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">timeout</span><span class="o">=</span><span class="n">timeout</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L104" class="blob-num js-line-number" data-line-number="104"></td>
        <td id="LC104" class="blob-code js-file-line">                <span class="k">if</span> <span class="n">msg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;parent_header&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span> <span class="ow">and</span> <span class="n">msg</span><span class="p">[</span><span class="s">&quot;parent_header&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;msg_id&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span> <span class="o">==</span> <span class="n">msg_id</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L105" class="blob-num js-line-number" data-line-number="105"></td>
        <td id="LC105" class="blob-code js-file-line">                    <span class="k">break</span></td>
      </tr>
      <tr>
        <td id="L106" class="blob-num js-line-number" data-line-number="106"></td>
        <td id="LC106" class="blob-code js-file-line">            <span class="k">except</span> <span class="n">Empty</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L107" class="blob-num js-line-number" data-line-number="107"></td>
        <td id="LC107" class="blob-code js-file-line">                <span class="k">raise</span> <span class="n">IPyNbException</span><span class="p">(</span><span class="s">&quot;Timeout of </span><span class="si">%d</span><span class="s"> seconds exceeded executing cell: </span><span class="si">%s</span><span class="s">&quot;</span> <span class="p">(</span><span class="n">timeout</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell</span><span class="o">.</span><span class="n">input</span><span class="p">))</span></td>
      </tr>
      <tr>
        <td id="L108" class="blob-num js-line-number" data-line-number="108"></td>
        <td id="LC108" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L109" class="blob-num js-line-number" data-line-number="109"></td>
        <td id="LC109" class="blob-code js-file-line">        <span class="n">reply</span> <span class="o">=</span> <span class="n">msg</span><span class="p">[</span><span class="s">&#39;content&#39;</span><span class="p">]</span></td>
      </tr>
      <tr>
        <td id="L110" class="blob-num js-line-number" data-line-number="110"></td>
        <td id="LC110" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L111" class="blob-num js-line-number" data-line-number="111"></td>
        <td id="LC111" class="blob-code js-file-line">        <span class="k">if</span> <span class="n">reply</span><span class="p">[</span><span class="s">&#39;status&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;error&#39;</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L112" class="blob-num js-line-number" data-line-number="112"></td>
        <td id="LC112" class="blob-code js-file-line">            <span class="k">raise</span> <span class="n">IPyNbException</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">cell_num</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell_description</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell</span><span class="o">.</span><span class="n">input</span><span class="p">,</span> <span class="s">&#39;</span><span class="se">\n</span><span class="s">&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">reply</span><span class="p">[</span><span class="s">&#39;traceback&#39;</span><span class="p">]))</span></td>
      </tr>
      <tr>
        <td id="L113" class="blob-num js-line-number" data-line-number="113"></td>
        <td id="LC113" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L114" class="blob-num js-line-number" data-line-number="114"></td>
        <td id="LC114" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">repr_failure</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">excinfo</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L115" class="blob-num js-line-number" data-line-number="115"></td>
        <td id="LC115" class="blob-code js-file-line">        <span class="sd">&quot;&quot;&quot; called when self.runtest() raises an exception. &quot;&quot;&quot;</span></td>
      </tr>
      <tr>
        <td id="L116" class="blob-num js-line-number" data-line-number="116"></td>
        <td id="LC116" class="blob-code js-file-line">        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">excinfo</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">IPyNbException</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L117" class="blob-num js-line-number" data-line-number="117"></td>
        <td id="LC117" class="blob-code js-file-line">            <span class="k">return</span> <span class="s">&quot;</span><span class="se">\n</span><span class="s">&quot;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span></td>
      </tr>
      <tr>
        <td id="L118" class="blob-num js-line-number" data-line-number="118"></td>
        <td id="LC118" class="blob-code js-file-line">                <span class="s">&quot;Notebook execution failed&quot;</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L119" class="blob-num js-line-number" data-line-number="119"></td>
        <td id="LC119" class="blob-code js-file-line">                <span class="s">&quot;Cell </span><span class="si">%d</span><span class="s">: </span><span class="si">%s</span><span class="se">\n\n</span><span class="s">&quot;</span></td>
      </tr>
      <tr>
        <td id="L120" class="blob-num js-line-number" data-line-number="120"></td>
        <td id="LC120" class="blob-code js-file-line">                <span class="s">&quot;Input:</span><span class="se">\n</span><span class="si">%s</span><span class="se">\n\n</span><span class="s">&quot;</span></td>
      </tr>
      <tr>
        <td id="L121" class="blob-num js-line-number" data-line-number="121"></td>
        <td id="LC121" class="blob-code js-file-line">                <span class="s">&quot;Traceback:</span><span class="se">\n</span><span class="si">%s</span><span class="se">\n</span><span class="s">&quot;</span> <span class="o">%</span> <span class="n">excinfo</span><span class="o">.</span><span class="n">value</span><span class="o">.</span><span class="n">args</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L122" class="blob-num js-line-number" data-line-number="122"></td>
        <td id="LC122" class="blob-code js-file-line">            <span class="p">])</span></td>
      </tr>
      <tr>
        <td id="L123" class="blob-num js-line-number" data-line-number="123"></td>
        <td id="LC123" class="blob-code js-file-line">        <span class="k">else</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L124" class="blob-num js-line-number" data-line-number="124"></td>
        <td id="LC124" class="blob-code js-file-line">            <span class="k">return</span> <span class="s">&quot;pytest plugin exception: </span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="nb">str</span><span class="p">(</span><span class="n">excinfo</span><span class="o">.</span><span class="n">value</span><span class="p">)</span></td>
      </tr>
      <tr>
        <td id="L125" class="blob-num js-line-number" data-line-number="125"></td>
        <td id="LC125" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L126" class="blob-num js-line-number" data-line-number="126"></td>
        <td id="LC126" class="blob-code js-file-line">    <span class="k">def</span> <span class="nf">reportinfo</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></td>
      </tr>
      <tr>
        <td id="L127" class="blob-num js-line-number" data-line-number="127"></td>
        <td id="LC127" class="blob-code js-file-line">        <span class="n">description</span> <span class="o">=</span> <span class="s">&quot;cell </span><span class="si">%d</span><span class="s">&quot;</span> <span class="o">%</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell_num</span></td>
      </tr>
      <tr>
        <td id="L128" class="blob-num js-line-number" data-line-number="128"></td>
        <td id="LC128" class="blob-code js-file-line">        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell_description</span><span class="p">:</span></td>
      </tr>
      <tr>
        <td id="L129" class="blob-num js-line-number" data-line-number="129"></td>
        <td id="LC129" class="blob-code js-file-line">            <span class="n">description</span> <span class="o">+=</span> <span class="s">&quot;: &quot;</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">cell_description</span></td>
      </tr>
      <tr>
        <td id="L130" class="blob-num js-line-number" data-line-number="130"></td>
        <td id="LC130" class="blob-code js-file-line">        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">fspath</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="n">description</span></td>
      </tr>
</table>

  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer" role="contentinfo">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/" aria-label="Homepage">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2014 <span title="0.07575s from github-fe131-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-suggester-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="fullscreen-contents js-fullscreen-contents js-suggester-field" placeholder=""></textarea>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-x flash-close js-ajax-error-dismiss" aria-label="Dismiss error"></a>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-ba50a1ca41995f0b006425c6db96c5669d18fd98.js" type="text/javascript"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github-84d7241f988dba4898a349b34fd24e7efb935fa0.js" type="text/javascript"></script>
      
      
        <script async src="https://www.google-analytics.com/analytics.js"></script>
  </body>
</html>

