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
    if request.method == 'POST':
        status_filter = request.POST.get('status')
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


    # Filter by bundle list
    if bundle_list_filter and not selected_category \
                        and not selected_category\
                        and not selected_contexts\
                        and not selected_version:
        bundle_lists = Bundles.objects.filter(bundle_list__bundle=bundle_list_filter).order_by('id')
        context['bundles'] = bundle_lists
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["total_bundles"]= bundle_lists.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_lists 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_lists 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_lists:
            context['found_items']  = False

    #Filter by tag
    if selected_tag and not bundle_list_filter \
                        and not selected_category\
                        and not selected_contexts\
                        and not selected_version:
        filter_by_tags = Bundles.objects.filter(tag__tag=selected_tag).order_by('id')
        context['bundles'] = filter_by_tags
        context['fav_id'] = favorites
        context["selected_tag"]= selected_tag
        context["total_bundles"]= filter_by_tags.count()
        context["template_count"]= len([bundle 
                                        for bundle in filter_by_tags 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in filter_by_tags 
                                    if bundle.bundle_type.bundle_type =="node snippets"]) 
        if not filter_by_tags:
            context['found_items']  = False

    if selected_category and not bundle_list_filter \
                            and not selected_tag\
                            and not selected_contexts\
                            and not selected_version:
        filter_by_category = Bundles.objects.filter(category__category=selected_category).order_by('id')
        context['bundles'] = filter_by_category
        context['fav_id'] = favorites
        context["selected_category"]= selected_category
        context["total_bundles"]= filter_by_category.count()
        context["template_count"]= len([bundle 
                                        for bundle in filter_by_category 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in filter_by_category 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not filter_by_category:
            context['found_items']  = False

    if selected_contexts and not bundle_list_filter \
                            and not selected_tag\
                            and not selected_category\
                            and not selected_version:
        filter_by_context = Bundles.objects.filter(context__context=selected_contexts).order_by('id')
        context['bundles'] = filter_by_context
        context['fav_id'] = favorites
        context["selected_contexts"]= selected_contexts
        context["total_bundles"]= filter_by_context.count()
        context["template_count"]= len([bundle 
                                        for bundle in filter_by_context 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in filter_by_context 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not filter_by_context:
            context['found_items']  = False

    if selected_version and not bundle_list_filter \
                            and not selected_tag\
                            and not selected_category\
                            and not selected_contexts:
        filter_by_version = Bundles.objects.filter(houdini_version__version=selected_version).order_by('id')
        context['bundles'] = filter_by_version
        context['fav_id'] = favorites
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= filter_by_version.count()
        context["template_count"]= len([bundle 
                                        for bundle in filter_by_version 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in filter_by_version 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not filter_by_version:
            context['found_items']  = False
    
    # -----------------------------------------------------------------------------------------------
    # Filter By two Fields Starts Here

    #filter bundles and tag
    if bundle_list_filter \
        and selected_tag \
        and not selected_category \
        and not selected_contexts \
        and not selected_version:
        bundle_tag_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(tag__tag=selected_tag)
        ).order_by('id')
        context['bundles'] = bundle_tag_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_tag"]= selected_tag
        context["total_bundles"]= bundle_tag_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_tag_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_tag_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_tag_filter:
            context['found_items']  = False
    
    # filter bundles with category
    if bundle_list_filter \
        and not selected_tag \
        and selected_category \
        and not selected_contexts \
        and not selected_version:
        bundle_category_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(category__category=selected_category)
        ).order_by('id')
        context['bundles'] = bundle_category_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_category"]= selected_category
        context["total_bundles"]= bundle_category_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_category_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_category_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_category_filter:
            context['found_items']  = False

    # filter bundles with context
    if bundle_list_filter \
        and not selected_tag \
        and not selected_category \
        and selected_contexts \
        and not selected_version:
        bundle_context_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(context__context=selected_contexts)
        ).order_by('id')
        context['bundles'] = bundle_context_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_contexts"]= selected_contexts
        context["total_bundles"]= bundle_context_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_context_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_context_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_context_filter:
            context['found_items']  = False

    # filter bundles with version
    if bundle_list_filter \
        and not selected_tag \
        and not selected_category \
        and not selected_contexts \
        and selected_version:
        bundle_houdini_version_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = bundle_houdini_version_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= bundle_houdini_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_houdini_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_houdini_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_houdini_version_filter:
            context['found_items']  = False                        
    
    # Filter by tag and category
    if selected_tag \
        and not bundle_list_filter\
        and selected_category \
        and not selected_contexts \
        and not selected_version:
        tags_category_filter = Bundles.objects.filter(
                                        Q(tag__tag=selected_tag) &
                                        Q(category__category=selected_category)
        ).order_by('id')
        context['bundles'] = tags_category_filter
        context['fav_id'] = favorites
        context["selected_tag"]= selected_tag
        context["selected_category"]= selected_category
        context["total_bundles"]= tags_category_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in tags_category_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in tags_category_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not tags_category_filter:
            context['found_items']  = False         

    # Filter by tag and context
    if selected_tag \
        and not bundle_list_filter\
        and not selected_category \
        and selected_contexts \
        and not selected_version:
        tags_contexts_filter = Bundles.objects.filter(
                                        Q(tag__tag=selected_tag) &
                                        Q(context__context=selected_contexts)
        ).order_by('id')
        context['bundles'] = tags_contexts_filter
        context['fav_id'] = favorites
        context["selected_tag"]= selected_tag
        context["selected_contexts"]= selected_contexts
        context["total_bundles"]= tags_contexts_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in tags_contexts_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in tags_contexts_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not tags_contexts_filter:
            context['found_items']  = False

    # Filter by tag and version
    if selected_tag \
        and not bundle_list_filter\
        and not selected_category \
        and not selected_contexts \
        and selected_version:
        tags_houdini_version_filter = Bundles.objects.filter(
                                        Q(tag__tag=selected_tag) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = tags_houdini_version_filter
        context['fav_id'] = favorites
        context["selected_tag"]= selected_tag
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= tags_houdini_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in tags_houdini_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in tags_houdini_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not tags_houdini_version_filter:
            context['found_items']  = False                            

    # Filter by category and version
    if selected_category\
        and not bundle_list_filter\
        and not selected_tag\
        and not selected_contexts \
        and selected_version:
        category_houdini_version_filter = Bundles.objects.filter(
                                        Q(category__category=selected_category) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = category_houdini_version_filter
        context['fav_id'] = favorites
        context["selected_category"]= selected_category
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= category_houdini_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in category_houdini_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in category_houdini_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not category_houdini_version_filter:
            context['found_items']  = False 
    
    # Filter by context and version
    if  selected_contexts\
        and not bundle_list_filter\
        and not selected_tag\
        and not selected_category \
        and selected_version:
        context_houdini_version_filter = Bundles.objects.filter(
                                        Q(context__context=selected_contexts) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = context_houdini_version_filter
        context['fav_id'] = favorites
        context["selected_contexts"]= selected_contexts
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= context_houdini_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in context_houdini_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in context_houdini_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not context_houdini_version_filter:
            context['found_items']  = False        

    #-------------------------------------------------------------------------------------
    # Filtering Three fields combination
    
    # Filter by bundle, tag and category
    if bundle_list_filter \
        and selected_tag \
        and selected_category \
        and not selected_contexts \
        and not selected_version:
        bundle_tag_category_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(tag__tag=selected_tag) &
                                        Q(category__category=selected_category)
        ).order_by('id')
        context['bundles'] = bundle_tag_category_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_tag"]= selected_tag
        context["selected_category"]= selected_category
        context["total_bundles"]= bundle_tag_category_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_tag_category_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_tag_category_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_tag_category_filter:
            context['found_items']  = False 

    # Filter by bundle, tag and context
    if bundle_list_filter \
        and selected_tag \
        and not selected_category \
        and selected_contexts \
        and not selected_version:
        bundle_tag_context_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(tag__tag=selected_tag) &
                                        Q(context__context=selected_contexts)
        ).order_by('id')
        context['bundles'] = bundle_tag_context_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_tag"]= selected_tag
        context["selected_contexts"]= selected_contexts
        context["total_bundles"]= bundle_tag_context_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_tag_context_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_tag_context_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_tag_context_filter:
            context['found_items']  = False

    # Filter by bundle, tag and version
    if bundle_list_filter \
        and selected_tag \
        and not selected_category \
        and not selected_contexts \
        and selected_version:
        bundle_tag_houdini_version_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(tag__tag=selected_tag) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = bundle_tag_houdini_version_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_tag"]= selected_tag
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= bundle_tag_houdini_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_tag_houdini_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_tag_houdini_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_tag_houdini_version_filter:
            context['found_items']  = False

    # Filter by tag, category and version
    if selected_tag \
        and not bundle_list_filter\
        and selected_category \
        and not selected_contexts \
        and selected_version:
        tag_category_houdini_version_filter = Bundles.objects.filter(
                                        Q(tag__tag=selected_tag) &
                                        Q(category__category=selected_category) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = tag_category_houdini_version_filter
        context['fav_id'] = favorites
        context["selected_tag"]= selected_tag
        context["selected_category"]= selected_category
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= tag_category_houdini_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in tag_category_houdini_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in tag_category_houdini_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not tag_category_houdini_version_filter:
            context['found_items']  = False


    # Filter by tag, context and version
    if selected_tag \
        and not bundle_list_filter\
        and not selected_category \
        and selected_contexts \
        and selected_version:
        tag_context_houdini_version_filter = Bundles.objects.filter(
                                        Q(tag__tag=selected_tag) &
                                        Q(context__context=selected_contexts) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = tag_context_houdini_version_filter
        context['fav_id'] = favorites
        context["selected_tag"]= selected_tag
        context["selected_contexts"]= selected_contexts
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= tag_context_houdini_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in tag_context_houdini_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in tag_context_houdini_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not tag_context_houdini_version_filter:
            context['found_items']  = False
    # --------------------------------------------------------------------------------------
    # Filtering four fields combination

    # Filter by bundle, tag, category and version
    if bundle_list_filter \
        and selected_tag \
        and selected_category \
        and not selected_contexts \
        and selected_version:
        bundle_tag_category_version_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(tag__tag=selected_tag) &
                                        Q(category__category=selected_category) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = bundle_tag_category_version_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_tag"]= selected_tag
        context["selected_category"]= selected_category
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= bundle_tag_category_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_tag_category_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_tag_category_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_tag_category_version_filter:
            context['found_items']  = False

    # Filter by bundle, tag, context and version
    if bundle_list_filter \
        and selected_tag \
        and not selected_category \
        and selected_contexts \
        and selected_version:
        bundle_tag_context_version_filter = Bundles.objects.filter(
                                        Q(bundle_list__bundle=bundle_list_filter) &
                                        Q(tag__tag=selected_tag) &
                                        Q(context__context=selected_contexts) &
                                        Q(houdini_version__version=selected_version)
        ).order_by('id')
        context['bundles'] = bundle_tag_context_version_filter
        context['fav_id'] = favorites
        context["bundle_list_filter"]= bundle_list_filter
        context["selected_tag"]= selected_tag
        context["selected_contexts"]= selected_contexts
        context["selected_version"]= str(selected_version)
        context["total_bundles"]= bundle_tag_context_version_filter.count()
        context["template_count"]= len([bundle 
                                        for bundle in bundle_tag_context_version_filter 
                                        if bundle.bundle_type.bundle_type =="templates"])
        context["node_count"]= len([bundle 
                                    for bundle in bundle_tag_context_version_filter 
                                    if bundle.bundle_type.bundle_type =="node snippets"])
        if not bundle_tag_context_version_filter:
            context['found_items']  = False

    # Render the template     
    return render(request, "houmanager\index.html", context)
