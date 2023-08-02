# Create the binary executable

TARGET	=	camera

SRC	=	camera.py \
		config.py \
		visca.py

all: $(TARGET)

$(TARGET): $(SRCS)
	build
