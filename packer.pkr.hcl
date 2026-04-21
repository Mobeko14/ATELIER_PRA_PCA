packer {
  required_plugins {
    docker = {
      source  = "github.com/hashicorp/docker"
      version = ">= 1.1.0"
    }
  }
}

variable "image_name" {
  type    = string
  default = "pra/flask-sqlite"
}

variable "image_tag" {
  type    = string
  default = "2.0"
}

source "docker" "flask" {
  image  = "python:3.12-slim"
  commit = true
}

build {
  name    = "pra-flask-sqlite"
  sources = ["source.docker.flask"]

  provisioner "file" {
    source      = "flask_app/"
    destination = "/app"
  }

  provisioner "shell" {
    inline = [
      "set -eux",
      "pip install --no-cache-dir --upgrade pip",
      "pip install --no-cache-dir -r /app/requirements.txt",
      "mkdir -p /data",
      "chmod 777 /data"
    ]
  }

  # 🔥 ICI le vrai CMD
  post-processor "docker-tag" {
    repository = var.image_name
    tags       = [var.image_tag]
  }
}
