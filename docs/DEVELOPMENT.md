## Development

### Testing

#### Unit Tests

The code is 100% unit test coverage complete, and no pull-requests will be
accepted that do not maintain this level of coverage. That said, its possible
(_likely_) that we have not covered every possible scenario in our unit tests
that could cause failures. We will strive to fill out every reasonable failure
scenario.

#### Integration Tests

Because its hard to predict cloud failures, we provide integration tests for
most of our modules. These integration tests actually go off and execute real
operations in your accounts, and rely on particular environments being setup
in order to run. These tests are great to run though to validate that your
credentials are all correct.

Specific integration test notes are below, describing what is required to run
each set of tests.

Executing the tests:

    HIPCHAT_TOKEN=<xxx> RIGHTSCALE_TOKEN=<xxx> make integration

    PYFLAKES_NODOCTEST=True python setup.py integration pep8 pyflakes
    running integration
    integration_01_clone_dry (integration_server_array.IntegrationServerArray) ... ok
    integration_02a_clone (integration_server_array.IntegrationServerArray) ... ok
    integration_02b_clone_with_duplicate_array (integration_server_array.IntegrationServerArray) ... ok
    integration_03a_update_params (integration_server_array.IntegrationServerArray) ... ok
    integration_03b_update_with_invalid_params (integration_server_array.IntegrationServerArray) ... ok
    integration_04_launch (integration_server_array.IntegrationServerArray) ... ok
    integration_05_destroy (integration_server_array.IntegrationServerArray) ... ok
    integration_test_execute_real (integration_hipchat.IntegrationHipchatMessage) ... ok
    integration_test_execute_with_invalid_creds (integration_hipchat.IntegrationHipchatMessage) ... ok
    integration_test_init_without_environment_creds (integration_hipchat.IntegrationHipchatMessage) ... ok

    Name                                     Stmts   Miss  Cover   Missing
    ----------------------------------------------------------------------
    kingpin                                      0      0   100%   
    kingpin.actors                               0      0   100%   
    kingpin.actors.base                         62      5    92%   90, 95, 146, 215-216
    kingpin.actors.exceptions                    4      0   100%   
    kingpin.actors.hipchat                      58      5    91%   59, 111-118
    kingpin.actors.misc                         17      5    71%   47-49, 57-62
    kingpin.actors.rightscale                    0      0   100%   
    kingpin.actors.rightscale.api              137     46    66%   153-164, 251-258, 343-346, 381-382, 422-445, 466-501
    kingpin.actors.rightscale.base              31      3    90%   36, 49, 79
    kingpin.actors.rightscale.server_array     195     49    75%   59-62, 68-72, 79, 174, 190-196, 213-216, 249-250, 253-256, 278-281, 303-305, 377-380, 437-440, 501-505, 513-547
    kingpin.utils                               67     30    55%   57-69, 78, 93-120, 192-202
    ----------------------------------------------------------------------
    TOTAL                                      571    143    75%   
    ----------------------------------------------------------------------
    Ran 10 tests in 880.274s

    OK
    running pep8
    running pyflakes

##### kingpin.actor.rightscale.server_array

These tests clone a ServerArray, modify it, launch it, and destroy it. They
rely on an existing ServerArray template being available and launchable in
your environment. For simple testing, I recommend just using a standard
RightScale ServerTemplate.

**Required RightScale Resources**

  * ServerArray: _kingpin-integration-testing_
    Any ServerArray that launches a server in your environment.
  * RightScript: _kingpin-integration-testing-script_
    Should be a script that sleeps for a specified amount of time.
    **Requires `SLEEP` input**

### Class/Object Architecture

    kingpin.rb
    |
    +-- deployment.Deployer
        | Executes a deployment based on the supplied DSL.
        |
        +-- actors.rightscale
        |   | RightScale Cloud Management Actor
        |   |
        |   +-- server_array
        |       +-- Clone
        |       +-- Destroy
        |       +-- Execute
        |       +-- Launch
        |       +-- Update
        |
        +-- actors.aws
        |   | Amazon Web Services Actor
        |
        +-- actors.email
        |   | Email Actor
        |
        +-- actors.hipchat
        |   | Hipchat Actor
        |   |
        |   +-- Message
        |
        +-- actors.librato
            | Librato Metric Actor

### Setup

    # Create a dedicated Python virtual environment and source it
    virtualenv --no-site-packages .venv
    unset PYTHONPATH
    source .venv/bin/activate

    # Install the dependencies
    make build

    # Run the tests
    make test

### Postfix on Mac OSX

If you want to develop on a Mac OSX host, you need to enable email the
*postfix* daemon on your computer. Here's how!

Modify */Syatem/Library/LaunchDaemons/org.postfix.master.plist*:

    --- /System/Library/LaunchDaemons/org.postfix.master.plist.bak	2014-06-02 11:45:24.000000000 -0700
    +++ /System/Library/LaunchDaemons/org.postfix.master.plist	2014-06-02 11:47:07.000000000 -0700
    @@ -9,8 +9,6 @@
            <key>ProgramArguments</key>
            <array>
                   <string>master</string>
    -              <string>-e</string>
    -              <string>60</string>
            </array>
            <key>QueueDirectories</key>
            <array>
    @@ -18,5 +16,8 @@
            </array>
            <key>AbandonProcessGroup</key>
            <true/>
    +
    +        <key>KeepAlive</key>
    +       <true/>
     </dict>
     </plist>

Restart the service:

    cd /System/Library/LaunchDaemons
    sudo launchctl unload org.postfix.master.plist 
    sudo launchctl load org.postfix.master.plist