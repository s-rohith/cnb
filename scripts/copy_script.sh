#!/bin/bash
docker run --rm -d --name temp-builder paketobuildpacks/builder-jammy-base:latest sleep 10
docker cp temp-builder:/cnb/buildpacks/ ./buildpacks
docker stop temp-builder
