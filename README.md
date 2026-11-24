# YARTICATED

CSI3680 Project

A python-based resource tracker for a [Proxmox VE](https://www.proxmox.com/) cluster that runs on a [QDevice](https://pve.proxmox.com/pve-docs/pve-admin-guide.html#_qdevice_technical_overview).

# Setup

### OPTIONAL: Create a new read-only user
*You may instead use the root user. If privilege separation is enabled, these should be essentially equivalent. However, this step does not hurt.*

Within the Proxmox web management console, navigate to `Datacenter` > `Permissions` > `Users`
*Add* a new user **USERNAME**.

Then, move to the parent setting `Permissions`, *Add* a new `User Permission` with `Path` **/** and User **USERNAME**. Leave Propagate enabled.

The recommended default role for this user is [PVEAuditor](https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_roles). This gives read-only access.


### Create a read-only API token

Within `Permissions` > `API Tokens`, *Add* an **API_TOKEN** for **USERNAME**. Token ID should be a descriptive identifier such as *readonly*.

Keep `Privilege Separation` enabled, set *Expire* according to your own use.
**Copy this key, it will not be shown again!**

Set the `Permissions` of this key similarly to [the read-only user](#optional-create-a-new-read-only-user), except now we are *Add*-ing an `API Token Permission`.

### .env configuration
Your .env will look like:
```
USERNAME={USERNAME}@{REALM}!{TOKEN_ID}
API_TOKEN={UUID}
```
For example:
```
USERNAME=bobbytables@pam!readonly
API_TOKEN=aabbccdd-d34d-b33f-1010-fafaddf12345
```