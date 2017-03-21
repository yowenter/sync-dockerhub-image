set -x
# remove duplicate image name and sort 
awk '!seen[$0]++' third_party.list |  sort  > third_party.list.bak
mv third_party.list.bak third_party.list

awk '!seen[$0]++' image_name_convert.list |  sort  > image_name_convert.list.bak

mv image_name_convert.list.bak image_name_convert.list


# remove duplicate image in library
awk '!seen[$0]++' image.list  > image.list.bak
mv image.list.bak image.list
