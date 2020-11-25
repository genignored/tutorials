# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# Modified for and by Oxford Nanopore Technologies
ARG BASE_CONTAINER=ontresearch/nanolabs-notebook
FROM $BASE_CONTAINER
LABEL maintainer="Oxford Nanopore Technologies"


# for notebooks etc - see below
USER root
ARG RESOURCE_DIR=/epi2me-resources
RUN \
  mkdir -p ${RESOURCE_DIR} \
  && rm -rf ${RESOURCE_DIR}/tutorials \
  && fix-permissions ${RESOURCE_DIR}

# notebooks - installed to ${RESOURCE_DIR}
USER $NB_UID
COPY --chown=$NB_UID tutorials $RESOURCE_DIR/tutorials
RUN \
  fix-permissions ${RESOURCE_DIR}/tutorials \
  && jupyter trust --reset \
  && for file in ${RESOURCE_DIR}/tutorials/*.ipynb; do \
      # we need to trust the file for e.g. bokeh plots to show
      jupyter trust ${file}; \
      # prevent users modifying canon
      chmod a-w ${file}; \
      ls -l ${file}; \
  done;

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
