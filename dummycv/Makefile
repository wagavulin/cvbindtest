TARGET := libdummycv.so
SRCS := dummycv.cpp
OBJS := $(SRCS:%.cpp=%.o)
DEPS := $(SRCS:%.cpp=%.d)

CXX := clang++
CXXFLAGS := -g -Wall -Wextra
CPPFLAGS :=
LDFLAGS :=
LIBS :=

all: $(TARGET)

-include $(DEPS)

$(TARGET): $(OBJS)
	$(CXX) $(LDFLAGS) --shared -o $@ $^ $(LIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c -MMD -MP $<

clean:
	rm -f $(PROG) $(OBJS) $(DEPS)
