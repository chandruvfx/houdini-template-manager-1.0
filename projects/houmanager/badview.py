# Filter by bundle list
    # if bundle_list_filter and not selected_category \
    #                     and not selected_category\
    #                     and not selected_contexts\
    #                     and not selected_version:
    #     bundle_lists = Bundles.objects.filter(bundle_list__bundle=bundle_list_filter).order_by('id')
    #     context['bundles'] = bundle_lists
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["total_bundles"]= bundle_lists.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_lists 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_lists 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_lists:
    #         context['found_items']  = False

    # #Filter by tag
    # if selected_tag and not bundle_list_filter \
    #                     and not selected_category\
    #                     and not selected_contexts\
    #                     and not selected_version:
    #     filter_by_tags = Bundles.objects.filter(tag__tag=selected_tag).order_by('id')
    #     context['bundles'] = filter_by_tags
    #     context['fav_id'] = favorites
    #     context["selected_tag"]= selected_tag
    #     context["total_bundles"]= filter_by_tags.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in filter_by_tags 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in filter_by_tags 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"]) 
    #     if not filter_by_tags:
    #         context['found_items']  = False

    # if selected_category and not bundle_list_filter \
    #                         and not selected_tag\
    #                         and not selected_contexts\
    #                         and not selected_version:
    #     filter_by_category = Bundles.objects.filter(category__category=selected_category).order_by('id')
    #     context['bundles'] = filter_by_category
    #     context['fav_id'] = favorites
    #     context["selected_category"]= selected_category
    #     context["total_bundles"]= filter_by_category.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in filter_by_category 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in filter_by_category 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not filter_by_category:
    #         context['found_items']  = False

    # if selected_contexts and not bundle_list_filter \
    #                         and not selected_tag\
    #                         and not selected_category\
    #                         and not selected_version:
    #     filter_by_context = Bundles.objects.filter(context__context=selected_contexts).order_by('id')
    #     context['bundles'] = filter_by_context
    #     context['fav_id'] = favorites
    #     context["selected_contexts"]= selected_contexts
    #     context["total_bundles"]= filter_by_context.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in filter_by_context 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in filter_by_context 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not filter_by_context:
    #         context['found_items']  = False

    # if selected_version and not bundle_list_filter \
    #                         and not selected_tag\
    #                         and not selected_category\
    #                         and not selected_contexts:
    #     filter_by_version = Bundles.objects.filter(houdini_version__version=selected_version).order_by('id')
    #     context['bundles'] = filter_by_version
    #     context['fav_id'] = favorites
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= filter_by_version.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in filter_by_version 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in filter_by_version 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not filter_by_version:
    #         context['found_items']  = False
    # # -----------------------------------------------------------------------------------------------
    # # Filter By two Fields Starts Here

    # # filter bundles and tag
    # if bundle_list_filter \
    #     and selected_tag \
    #     and not selected_category \
    #     and not selected_contexts \
    #     and not selected_version:
    #     bundle_tag_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(tag__tag=selected_tag)
    #     ).order_by('id')
    #     context['bundles'] = bundle_tag_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_tag"]= selected_tag
    #     context["total_bundles"]= bundle_tag_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_tag_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_tag_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_tag_filter:
    #         context['found_items']  = False
    
    # # filter bundles with category
    # if bundle_list_filter \
    #     and not selected_tag \
    #     and selected_category \
    #     and not selected_contexts \
    #     and not selected_version:
    #     bundle_category_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(category__category=selected_category)
    #     ).order_by('id')
    #     context['bundles'] = bundle_category_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_category"]= selected_category
    #     context["total_bundles"]= bundle_category_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_category_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_category_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_category_filter:
    #         context['found_items']  = False

    # # filter bundles with context
    # if bundle_list_filter \
    #     and not selected_tag \
    #     and not selected_category \
    #     and selected_contexts \
    #     and not selected_version:
    #     bundle_context_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(context__context=selected_contexts)
    #     ).order_by('id')
    #     context['bundles'] = bundle_context_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_contexts"]= selected_contexts
    #     context["total_bundles"]= bundle_context_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_context_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_context_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_context_filter:
    #         context['found_items']  = False

    # # filter bundles with version
    # if bundle_list_filter \
    #     and not selected_tag \
    #     and not selected_category \
    #     and not selected_contexts \
    #     and selected_version:
    #     bundle_houdini_version_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = bundle_houdini_version_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= bundle_houdini_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_houdini_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_houdini_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_houdini_version_filter:
    #         context['found_items']  = False                        
    
    # # Filter by tag and category
    # if selected_tag \
    #     and not bundle_list_filter\
    #     and selected_category \
    #     and not selected_contexts \
    #     and not selected_version:
    #     tags_category_filter = Bundles.objects.filter(
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(category__category=selected_category)
    #     ).order_by('id')
    #     context['bundles'] = tags_category_filter
    #     context['fav_id'] = favorites
    #     context["selected_tag"]= selected_tag
    #     context["selected_category"]= selected_category
    #     context["total_bundles"]= tags_category_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in tags_category_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in tags_category_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not tags_category_filter:
    #         context['found_items']  = False         

    # # Filter by tag and context
    # if selected_tag \
    #     and not bundle_list_filter\
    #     and not selected_category \
    #     and selected_contexts \
    #     and not selected_version:
    #     tags_contexts_filter = Bundles.objects.filter(
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(context__context=selected_contexts)
    #     ).order_by('id')
    #     context['bundles'] = tags_contexts_filter
    #     context['fav_id'] = favorites
    #     context["selected_tag"]= selected_tag
    #     context["selected_contexts"]= selected_contexts
    #     context["total_bundles"]= tags_contexts_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in tags_contexts_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in tags_contexts_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not tags_contexts_filter:
    #         context['found_items']  = False

    # # Filter by tag and version
    # if selected_tag \
    #     and not bundle_list_filter\
    #     and not selected_category \
    #     and not selected_contexts \
    #     and selected_version:
    #     tags_houdini_version_filter = Bundles.objects.filter(
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = tags_houdini_version_filter
    #     context['fav_id'] = favorites
    #     context["selected_tag"]= selected_tag
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= tags_houdini_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in tags_houdini_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in tags_houdini_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not tags_houdini_version_filter:
    #         context['found_items']  = False                            

    # # Filter by category and version
    # if selected_category\
    #     and not bundle_list_filter\
    #     and not selected_tag\
    #     and not selected_contexts \
    #     and selected_version:
    #     category_houdini_version_filter = Bundles.objects.filter(
    #                                     Q(category__category=selected_category) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = category_houdini_version_filter
    #     context['fav_id'] = favorites
    #     context["selected_category"]= selected_category
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= category_houdini_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in category_houdini_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in category_houdini_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not category_houdini_version_filter:
    #         context['found_items']  = False 
    
    # # Filter by context and version
    # if  selected_contexts\
    #     and not bundle_list_filter\
    #     and not selected_tag\
    #     and not selected_category \
    #     and selected_version:
    #     context_houdini_version_filter = Bundles.objects.filter(
    #                                     Q(context__context=selected_contexts) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = context_houdini_version_filter
    #     context['fav_id'] = favorites
    #     context["selected_contexts"]= selected_contexts
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= context_houdini_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in context_houdini_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in context_houdini_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not context_houdini_version_filter:
    #         context['found_items']  = False        

    # #-------------------------------------------------------------------------------------
    # # Filtering Three fields combination
    
    # # Filter by bundle, tag and category
    # if bundle_list_filter \
    #     and selected_tag \
    #     and selected_category \
    #     and not selected_contexts \
    #     and not selected_version:
    #     bundle_tag_category_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(category__category=selected_category)
    #     ).order_by('id')
    #     context['bundles'] = bundle_tag_category_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_tag"]= selected_tag
    #     context["selected_category"]= selected_category
    #     context["total_bundles"]= bundle_tag_category_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_tag_category_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_tag_category_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_tag_category_filter:
    #         context['found_items']  = False 

    # # Filter by bundle, tag and context
    # if bundle_list_filter \
    #     and selected_tag \
    #     and not selected_category \
    #     and selected_contexts \
    #     and not selected_version:
    #     bundle_tag_context_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(context__context=selected_contexts)
    #     ).order_by('id')
    #     context['bundles'] = bundle_tag_context_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_tag"]= selected_tag
    #     context["selected_contexts"]= selected_contexts
    #     context["total_bundles"]= bundle_tag_context_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_tag_context_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_tag_context_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_tag_context_filter:
    #         context['found_items']  = False

    # # Filter by bundle, tag and version
    # if bundle_list_filter \
    #     and selected_tag \
    #     and not selected_category \
    #     and not selected_contexts \
    #     and selected_version:
    #     bundle_tag_houdini_version_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = bundle_tag_houdini_version_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_tag"]= selected_tag
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= bundle_tag_houdini_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_tag_houdini_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_tag_houdini_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_tag_houdini_version_filter:
    #         context['found_items']  = False

    # # Filter by tag, category and version
    # if selected_tag \
    #     and not bundle_list_filter\
    #     and selected_category \
    #     and not selected_contexts \
    #     and selected_version:
    #     tag_category_houdini_version_filter = Bundles.objects.filter(
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(category__category=selected_category) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = tag_category_houdini_version_filter
    #     context['fav_id'] = favorites
    #     context["selected_tag"]= selected_tag
    #     context["selected_category"]= selected_category
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= tag_category_houdini_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in tag_category_houdini_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in tag_category_houdini_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not tag_category_houdini_version_filter:
    #         context['found_items']  = False


    # # Filter by tag, context and version
    # if selected_tag \
    #     and not bundle_list_filter\
    #     and not selected_category \
    #     and selected_contexts \
    #     and selected_version:
    #     tag_context_houdini_version_filter = Bundles.objects.filter(
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(context__context=selected_contexts) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = tag_context_houdini_version_filter
    #     context['fav_id'] = favorites
    #     context["selected_tag"]= selected_tag
    #     context["selected_contexts"]= selected_contexts
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= tag_context_houdini_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in tag_context_houdini_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in tag_context_houdini_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not tag_context_houdini_version_filter:
    #         context['found_items']  = False
    # # --------------------------------------------------------------------------------------
    # # Filtering four fields combination

    # # Filter by bundle, tag, category and version
    # if bundle_list_filter \
    #     and selected_tag \
    #     and selected_category \
    #     and not selected_contexts \
    #     and selected_version:
    #     bundle_tag_category_version_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(category__category=selected_category) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = bundle_tag_category_version_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_tag"]= selected_tag
    #     context["selected_category"]= selected_category
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= bundle_tag_category_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_tag_category_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_tag_category_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_tag_category_version_filter:
    #         context['found_items']  = False

    # # Filter by bundle, tag, context and version
    # if bundle_list_filter \
    #     and selected_tag \
    #     and not selected_category \
    #     and selected_contexts \
    #     and selected_version:
    #     bundle_tag_context_version_filter = Bundles.objects.filter(
    #                                     Q(bundle_list__bundle=bundle_list_filter) &
    #                                     Q(tag__tag=selected_tag) &
    #                                     Q(context__context=selected_contexts) &
    #                                     Q(houdini_version__version=selected_version)
    #     ).order_by('id')
    #     context['bundles'] = bundle_tag_context_version_filter
    #     context['fav_id'] = favorites
    #     context["bundle_list_filter"]= bundle_list_filter
    #     context["selected_tag"]= selected_tag
    #     context["selected_contexts"]= selected_contexts
    #     context["selected_version"]= str(selected_version)
    #     context["total_bundles"]= bundle_tag_context_version_filter.count()
    #     context["template_count"]= len([bundle 
    #                                     for bundle in bundle_tag_context_version_filter 
    #                                     if bundle.bundle_type.bundle_type =="templates"])
    #     context["node_count"]= len([bundle 
    #                                 for bundle in bundle_tag_context_version_filter 
    #                                 if bundle.bundle_type.bundle_type =="node snippets"])
    #     if not bundle_tag_context_version_filter:
    #         context['found_items']  = False