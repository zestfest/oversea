resource "linode_linode" "admin" {
        image = "Ubuntu 18.04 LTS"
        kernel = "4.16.11-x86_64-linode108"
        name = "admin"
        group = "oversea1"
        region = "Atlanta, GA, USA"
        size = 2048
        ssh_key = "${var.ssh_key}"
        root_password = "${var.root_password}"
        manage_private_ip_automatically = "true"
        provisioner "file" {
          source      = "files/hosts"
          destination = "/tmp/hosts"
        }
        provisioner "file" {
          source      = "files/zerotier-one_1.2.12_amd64.deb"
          destination = "/tmp/zerotier-one_1.2.12_amd64.deb"
        }
        provisioner "file" {
          source      = "files/postinstall.sh"
          destination = "/tmp/postinstall.sh"
        }
        provisioner "file" {
          source      = "files/install_salt_master.sh"
          destination = "/tmp/install_salt_master.sh"
        }
         # OverSea
         provisioner "file" {
           source      = "files/oversea/oversea_minions.sls"
           destination = "/tmp/oversea_minions.sls"
         }
         provisioner "file" {
           source      = "files/oversea/cluster.yml"
           destination = "/tmp/cluster.yml"
         }
         provisioner "file" {
           source      = "files/oversea/policy.cfg"
           destination = "/tmp/policy.cfg"
         }
        provisioner "remote-exec" {
        inline = [
          "chmod +x /tmp/postinstall.sh",
          "/tmp/postinstall.sh admin ${var.zerotier_network} ${var.size}",
        ]
        }
}

