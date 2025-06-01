from django.shortcuts import render
from pprint import pprint
from django.db.models import Q
import json
import os 


# Create your views here.
from .models import (BundlesList,
                     Tags,
                     Categories,
                     Contexts,
                     Versions,
                     BundleTypes,
                     Bundles)


# NOTE: Hard coded path has to removed
fav_file = r"D:\django_projects\projects\houmanager\static\houmanager\favotite.json"

def json_ops(in_data: dict):

    """Json Read Write Operations for favorites

    Args:
            data (dict): {fav_id: bundle_name}

    Function write favorite-{id} and bundle name in the 
    favorite.json file if not exist. otherwise it deletes.
    functionality implementation of clicking favorite to add in the json.
    clicking again in the same favorite remove the entry from json.
    """

    def write_json_file(data):
        """Write json files

        Args:
            data (dict): dump dict into json file
        """
        with open(fav_file, 'w') as file:
            json.dump(data, file, indent=4)

    if os.stat(fav_file).st_size != 0:
        """
        If json file is empty then read it
        """
        with open(fav_file, 'r') as file:
            """Read json files """
            data = json.load(file)
        
        # Write Value in json
        if not data or list(in_data.keys())[0] not in data:
            data[list(in_data.keys())[0]] = list(in_data.values())[0]
            write_json_file(data)
        
        # Delete Key in Json if exist
        elif list(in_data.keys())[0] in data:
            del data[list(in_data.keys())[0]]
            write_json_file(data)
    else:
        # If json is empty then write data
        data = in_data
        write_json_file(data)


def index(request):

    bundle_list = BundlesList.objects.all().order_by('id') 
    tags = Tags.objects.all().order_by('id')
    categories = Categories.objects.all().order_by('id')
    contexts = Contexts.objects.all().order_by('id')
    versions = Versions.objects.all().order_by('id')
    bundletypes = BundleTypes.objects.all().order_by('id')
    bundles = Bundles.objects.all().order_by('id')
    
    # All templates counts
    template_count = Bundles.objects.filter(bundle_type__bundle_type='templates').count() 

    # All node snippet counts 
    node_count = Bundles.objects.filter(bundle_type__bundle_type='node snippets').count()

    template_tag = bundletypes[0]
    nodesnippet_tag = bundletypes[1]

    
    context = {'bundle_list': bundle_list,
                'tags': tags,
                'categories': categories,
                'contexts': contexts,
                'versions': versions,
                'template_tag': template_tag,
                'nodesnippet_tag': nodesnippet_tag,
                "bundles": bundles, 
                "total_bundles": bundles.count(), #Total bundles shows dashboard
                "template_count": template_count,
                "node_count": node_count,
                "found_items": True #Bool used to show if search item not found.
    }
    
    if os.path.exists(fav_file) and os.stat(fav_file).st_size!=0:
        # Read favorite file 
        with open(fav_file, "r") as file:
            get_fav_data = json.load(file)
            context['faviorites'] = get_fav_data

    # Add all readed files in the favorite from the files
    favorites = []
    for id,bundle in get_fav_data.items():
        id = id.split('-')[-1]
        favorites.append(int(id))
        context['fav_id'] = favorites
    
    # Filter by templates and node snippet
    #
    # All, templates, nodesnippet , favorites controls
    status_filter = request.POST.get('status')
    if request.method == 'POST':
        if status_filter == "all":
            context['bundles'] = bundles
            context['fav_id'] = favorites
            context["total_bundles"]= bundles.count()
            context["status_filter"]= status_filter
            context["template_count"]= template_count
            context["node_count"]= node_count

        elif status_filter != 'all' and  status_filter != 'favorite':
            bundles = Bundles.objects.filter(bundle_type__bundle_type=status_filter).order_by('id')
            context['bundles'] = bundles
            context['fav_id'] = favorites
            context["total_bundles"]= bundles.count()
            context["status_filter"]= status_filter
            context["template_count"]= len([bundle 
                                            for bundle in bundles 
                                            if bundle.bundle_type.bundle_type =="templates"])
            context["node_count"]= len([bundle 
                                        for bundle in bundles 
                                        if bundle.bundle_type.bundle_type =="node snippets"])

        elif status_filter == 'favorite':
            # Filter favorites 
            fav_bundles = []
            for id,bundle in get_fav_data.items():
                id = id.split('-')[-1]
                fav_bundles.append([i for i in bundles if i.name == bundle and i.id == int(id)][0])
            context['bundles'] = fav_bundles
            context['fav_id'] = favorites
            context["total_bundles"]= len(fav_bundles)
            context["status_filter"]= status_filter
            context["template_count"]= len([bundle 
                                            for bundle in fav_bundles 
                                            if bundle.bundle_type.bundle_type =="templates"])
            context["node_count"]= len([bundle 
                                        for bundle in fav_bundles 
                                        if bundle.bundle_type.bundle_type =="node snippets"])

        

        # Ajax requst from the javascript to read the datas for favorite
        #
        # dict is passed. {fav_id: bundlename}
        #{
        #    "favorite-11": "cloth tear setup",
        #    "favorite-2": "perlin noise",
        #    "favorite-20": "swirl particles"
        #}
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data_dict = json.load(request)
            favid = data_dict['favid']
            bundlename = data_dict['bundlename']
            #write operations
            json_ops({favid: bundlename})


    # Search Operation Filter
    search = request.GET.get('search')
        
    if search:
        searched_bundle = Bundles.objects.filter(
                                    Q(description__icontains=search) |
                                    Q(name__icontains=search)
        ).order_by('id')
        context['bundles'] = searched_bundle
        context['fav_id'] = favorites
        context["total_bundles"]= searched_bundle.count()
        context["template_count"]= len([bundle 
                                        for bundle in searched_bundle 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in searched_bundle 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not searched_bundle:
            context['found_items']  = False


    # Read values from the filter submission
    bundle_list_filter = request.GET.get('bundles1', '')
    selected_tag = request.GET.get('selected_tag', '')
    selected_category = request.GET.get('selected_category', '')
    selected_contexts = request.GET.get('selected_contexts', '')
    selected_version = request.GET.get('selected_version', '')

    # Start with base queryset
    if not status_filter and not search:
        queryset = Bundles.objects.all()
        
        # Build dynamic filters
        filters = Q()
        
        if bundle_list_filter:
            filters &= Q(bundle_list__bundle=bundle_list_filter)
        if selected_tag:
            filters &= Q(tag__tag=selected_tag)
        if selected_category:
            filters &= Q(category__category=selected_category)
        if selected_contexts:
            filters &= Q(context__context=selected_contexts)
        if selected_version:
            filters &= Q(houdini_version__version=selected_version)
        
        # Apply filters
        filtered_bundles = queryset.filter(filters).distinct().order_by('id')
        context['bundles'] = filtered_bundles
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_tag"]= selected_tag
        context["selected_category"]= selected_category
        context["selected_contexts"]= selected_contexts
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= filtered_bundles.count()
        context["template_count"]= len([bundle 
                                        for bundle in filtered_bundles 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in filtered_bundles 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not filtered_bundles:
                context['found_items']  = False
            
    # Render the template     
    return render(request, "houmanager\index.html", context)
