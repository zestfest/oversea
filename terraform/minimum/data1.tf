resource "linode_linode" "data1" {
        image = "Ubuntu 18.04 LTS"
        kernel = "Latest 64 bit"
        name = "data1"
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
        provisioner "remote-exec" {
        inline = [
          "chmod +x /tmp/postinstall.sh",
          "/tmp/postinstall.sh data1 ${var.zerotier_network}",
        ]
        }
}

