# VERSION 0.1
# AUTHOR: Adam N. Hornsby (adamnhornsby) (Love Lab, UCL)
# DESCRIPTION: Container for re-creating experimental results from Hornsby & Love (2019) coherent representations paper
# BUILD: <build command>
# SOURCE: <github url>

FROM python:2.7-slim
LABEL maintainer="adamnhornsby"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV HOME /usr/local/data/

# Install Python dependencies
RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        gfortran \
	    r-base \
        littler \
        r-base-core \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

# Install code requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN Rscript -e "install.packages('Rfit', repos = 'http://cran.r-project.org')"

# set working directory
COPY politics/ /usr/local/data/politics/
COPY robots/ /usr/local/data/robots/
COPY simulation/ /usr/local/data/simulation/

COPY data/ /usr/local/data/

COPY entrypoint.sh /entrypoint.sh

WORKDIR /usr/local/data/
ENTRYPOINT ["/entrypoint.sh"]
